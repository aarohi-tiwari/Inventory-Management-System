import json
import csv
import io
from django.http import JsonResponse
from inventory.services.product_service import ProductService
from mongoengine.errors import DoesNotExist

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from inventory.models.product_model import Product


def home(request):
    return render(request, "index.html")  # just filename


def _safe_category_data(product):
    try:
        if product.category:
            return str(product.category.id), product.category.title
    except DoesNotExist:
        # Keep list APIs resilient if category reference is stale.
        return None, None
    return None, None

@csrf_exempt
def create_product(request):
    try:
        data = json.loads(request.body)
        product, errors = ProductService.create_product(data)

        if errors:
            return JsonResponse({"errors": errors}, status=400)

        return JsonResponse({
            "message": "Product created",
            "id": str(product.id),
            "created_at": product.created_at.isoformat() if product.created_at else None,
            "updated_at": product.updated_at.isoformat() if product.updated_at else None
        }, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@csrf_exempt
def update_product(request, product_id):
    try:
        data = json.loads(request.body)
        product, errors = ProductService.update_product(product_id, data)

        if errors:
            return JsonResponse({"errors": errors}, status=400)

        return JsonResponse({
            "message": "Updated successfully",
            "id": str(product.id),
            "created_at": product.created_at.isoformat() if product.created_at else None,
            "updated_at": product.updated_at.isoformat() if product.updated_at else None
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def delete_product(request, product_id):
    error = ProductService.delete_product(product_id)

    if error:
        return JsonResponse(error, status=404)

    return JsonResponse({"message": "Deleted (soft) successfully"})

@csrf_exempt
def list_products(request):
    try:
        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", 5))
        search = request.GET.get("search")
        brand = request.GET.get("brand")
        category = request.GET.get("category")
        created_after = request.GET.get("created_after")
        updated_after = request.GET.get("updated_after")
        sort_by = request.GET.get("sort_by", "-created_at")

        # ✅ Use service layer
        products, total, total_pages, errors = ProductService.get_products(
            page, limit, search, brand, category, created_after, updated_after, sort_by
        )
        if errors:
            return JsonResponse({"errors": errors}, status=400)

        data = []
        for p in products:
            category_id, category_name = _safe_category_data(p)
            data.append({
                "id": str(p.id),
                "name": p.name,
                "price": float(p.price),
                "brand": p.brand,
                "category": category_id,
                "category_name": category_name,
                "quantity": p.quantity,
                "created_at": p.created_at.isoformat() if p.created_at else None,
                "updated_at": p.updated_at.isoformat() if p.updated_at else None
            })

        return JsonResponse({
            "products": data,
            "total": total,
            "page": page,
            "total_pages": total_pages
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)
    
@csrf_exempt
def get_products_by_category(request, category_id):
    products = Product.objects(category=category_id, is_deleted=False)

    data = []
    for p in products:
        _, category_name = _safe_category_data(p)
        data.append({
            "id": str(p.id),
            "name": p.name,
            "category": category_name
        })

    return JsonResponse({"products": data})


@csrf_exempt
def bulk_create_products(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    upload = request.FILES.get("file")
    if not upload:
        return JsonResponse({"error": "CSV file is required as form-data key 'file'"}, status=400)

    try:
        decoded = upload.read().decode("utf-8")
    except UnicodeDecodeError:
        return JsonResponse({"error": "Unable to decode file as UTF-8 CSV"}, status=400)

    reader = csv.DictReader(io.StringIO(decoded))
    required_columns = {"name", "price", "brand", "category"}
    if not required_columns.issubset(set(reader.fieldnames or [])):
        return JsonResponse(
            {"error": "CSV must include columns: name, price, brand, category (optional: quantity)"},
            status=400,
        )

    created = []
    errors = []

    for idx, row in enumerate(reader, start=2):
        payload = {
            "name": (row.get("name") or "").strip(),
            "brand": (row.get("brand") or "").strip(),
        }

        try:
            payload["price"] = float((row.get("price") or "").strip())
        except ValueError:
            errors.append({"row": idx, "error": "Invalid price"})
            continue

        quantity_raw = (row.get("quantity") or "").strip()
        if quantity_raw:
            try:
                payload["quantity"] = int(quantity_raw)
            except ValueError:
                errors.append({"row": idx, "error": "Invalid quantity"})
                continue

        payload["category"] = (row.get("category") or "").strip()

        product, validation_errors = ProductService.create_product(payload)
        if validation_errors:
            errors.append({"row": idx, "errors": validation_errors})
            continue

        created.append(
            {
                "id": str(product.id),
                "name": product.name,
                "created_at": product.created_at.isoformat() if product.created_at else None,
            }
        )

    return JsonResponse(
        {
            "message": "Bulk upload processed",
            "created_count": len(created),
            "error_count": len(errors),
            "created": created,
            "errors": errors,
        },
        status=201 if created else 400,
    )