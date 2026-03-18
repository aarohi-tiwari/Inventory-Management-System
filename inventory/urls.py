from django.urls import path
from inventory.controllers import product_controller

urlpatterns = [
    path('products/', product_controller.create_product),
    path('products/list/', product_controller.list_products),  # ✅ ADD THIS
    path('products/<str:product_id>/', product_controller.update_product),
    path('products/delete/<str:product_id>/', product_controller.delete_product),
]