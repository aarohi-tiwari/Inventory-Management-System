from django.shortcuts import render


def products_ui(request):
    return render(request, "products_ui_react.html")

