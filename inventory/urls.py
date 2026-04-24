from django.urls import path
from inventory.controllers import product_controller
from inventory.controllers import product_category_controller

urlpatterns = [
    path('products/', product_controller.create_product),
    path('products/list/', product_controller.list_products),  
    path('products/<str:product_id>/', product_controller.update_product),
    path('products/delete/<str:product_id>/', product_controller.delete_product),
    path('products/bulk-upload/', product_controller.bulk_create_products),
    path('products/category/<str:category_id>/', product_controller.get_products_by_category),

    path('categories/', product_category_controller.categories_root),
    path('categories/list/', product_category_controller.list_categories),
    path('categories/<str:category_id>/', product_category_controller.get_category),
    path('categories/<str:category_id>/update/', product_category_controller.update_category),
    path('categories/<str:category_id>/delete/', product_category_controller.delete_category),
    path('categories/<str:category_id>/products/', product_category_controller.products_by_category),
    path('categories/<str:category_id>/products/<str:product_id>/add/', product_category_controller.add_product_to_category),
    path('categories/<str:category_id>/products/<str:product_id>/remove/', product_category_controller.remove_product_from_category),
]