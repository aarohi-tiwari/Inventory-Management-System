import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from inventory.services.product_category_service import ProductCategoryService


def _categories_payload():
    categories = ProductCategoryService.get_categories()
    data = []
    for c in categories:
        data.append(
            {
                "id": str(c.id),
                "title": c.title,
                "created_at": c.created_at.isoformat() if c.created_at else None,
                "updated_at": c.updated_at.isoformat() if c.updated_at else None,
            }
        )
    return data


@csrf_exempt
def categories_root(request):
    """GET: list (frontend dropdown). POST: create."""
    if request.method == "GET":
        return JsonResponse({"categories": _categories_payload()})

    if request.method == "POST":
        data = json.loads(request.body)
        category, errors = ProductCategoryService.create_category(data)

        if errors:
            return JsonResponse({"errors": errors}, status=400)

        return JsonResponse(
            {
                "message": "Category created",
                "id": str(category.id),
                "title": category.title,
            },
            status=201,
        )

    return JsonResponse({"error": "Method not allowed"}, status=405)


@csrf_exempt
def create_category(request):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)

    data = json.loads(request.body)
    category, errors = ProductCategoryService.create_category(data)

    if errors:
        return JsonResponse({"errors": errors}, status=400)

    return JsonResponse(
        {
            "message": "Category created",
            "id": str(category.id),
            "title": category.title,
        },
        status=201,
    )


def list_categories(request):
    return JsonResponse({"categories": _categories_payload()})


def get_category(request, category_id):
    category, error = ProductCategoryService.get_category(category_id)
    if error:
        return JsonResponse(error, status=404)
    return JsonResponse(
        {
            "id": str(category.id),
            "title": category.title,
            "created_at": category.created_at.isoformat() if category.created_at else None,
            "updated_at": category.updated_at.isoformat() if category.updated_at else None,
        }
    )


@csrf_exempt
def update_category(request, category_id):
    if request.method != "PUT":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    data = json.loads(request.body)
    category, errors = ProductCategoryService.update_category(category_id, data)
    if errors:
        status = 404 if errors.get("error") else 400
        return JsonResponse({"errors": errors}, status=status)
    return JsonResponse(
        {
            "message": "Category updated",
            "id": str(category.id),
            "title": category.title,
        }
    )


@csrf_exempt
def delete_category(request, category_id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    error = ProductCategoryService.delete_category(category_id)
    if error:
        return JsonResponse(error, status=404)
    return JsonResponse({"message": "Category deleted"})


def products_by_category(request, category_id):
    products, error = ProductCategoryService.list_products_by_category(category_id)
    if error:
        return JsonResponse(error, status=404)
    data = []
    for p in products:
        data.append(
            {
                "id": str(p.id),
                "name": p.name,
                "price": float(p.price),
                "brand": p.brand,
                "quantity": p.quantity,
            }
        )
    return JsonResponse({"products": data})


@csrf_exempt
def add_product_to_category(request, category_id, product_id):
    if request.method != "POST":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    product, error = ProductCategoryService.add_product_to_category(category_id, product_id)
    if error:
        status = 404 if "not found" in error.get("error", "").lower() else 400
        return JsonResponse(error, status=status)
    return JsonResponse(
        {
            "message": "Product added to category",
            "product_id": str(product.id),
            "category_id": str(product.category.id) if product.category else None,
        }
    )


@csrf_exempt
def remove_product_from_category(request, category_id, product_id):
    if request.method != "DELETE":
        return JsonResponse({"error": "Method not allowed"}, status=405)
    product, error = ProductCategoryService.remove_product_from_category(category_id, product_id)
    if error:
        return JsonResponse(error, status=404)
    return JsonResponse(
        {
            "message": "Product removed from category",
            "product_id": str(product.id),
            "category_id": None,
        }
    )