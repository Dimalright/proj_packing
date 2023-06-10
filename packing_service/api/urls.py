from django.urls import path

from .views import OrdersView, SkuView

urlpatterns = [
    path('v1/orders/<str:orderkey>/', OrdersView.as_view(), name='orders'),
    path('v1/sku/<str:sku>/', SkuView.as_view(), name='sku-detail'),
]
