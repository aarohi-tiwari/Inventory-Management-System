import json
from django.http import JsonResponse
from inventory.services.product_service import ProductService

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django.core.paginator import Paginator
from django.http import JsonResponse
from inventory.models.product_model import Product


def home(request):
    return render(request, "index.html")  # ✅ just filename

@csrf_exempt
def create_product(request):
    try:
        data = json.loads(request.body)
        product, errors = ProductService.create_product(data)

        if errors:
            return JsonResponse({"errors": errors}, status=400)

        return JsonResponse({"message": "Product created"}, status=201)

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



@csrf_exempt
def update_product(request, product_id):
    try:
        data = json.loads(request.body)
        product, errors = ProductService.update_product(product_id, data)

        if errors:
            return JsonResponse({"errors": errors}, status=400)

        return JsonResponse({"message": "Updated successfully"})

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)

@csrf_exempt
def delete_product(request, product_id):
    error = ProductService.delete_product(product_id)

    if error:
        return JsonResponse(error, status=404)

    return JsonResponse({"message": "Deleted (soft) successfully"})

@csrf_exempt
@csrf_exempt
def list_products(request):
    try:
        page = int(request.GET.get("page", 1))
        limit = int(request.GET.get("limit", 5))
        search = request.GET.get("search")
        brand = request.GET.get("brand")
        category = request.GET.get("category")

        # ✅ Use service layer
        products, total, total_pages = ProductService.get_products(
            page, limit, search, brand, category
        )

        data = []
        for p in products:
            data.append({
                "id": str(p.id),
                "name": p.name,
                "price": float(p.price),
                "brand": p.brand,
                "category": p.category,
                "quantity": p.quantity
            })

        return JsonResponse({
            "products": data,
            "total": total,
            "page": page,
            "total_pages": total_pages
        })

    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)