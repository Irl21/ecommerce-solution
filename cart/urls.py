from django.urls import path, include
from . import views



app_name='cart'

urlpatterns = [
    path('', views.CartView.as_view(), name='summary'),
    path('shop/', views.ProductView.as_view(), name='product-list'),
    path('shop/<slug>/', views.ProductDetailView.as_view(), name='product-detail'),
    path('increase-quantity/<pk>/', views.IncreaseQuantityView.as_view(), name='increase-quantity'),
    path('decrease-quantity/<pk>/', views.DecreaseQuantityView.as_view(), name='decrease-quantity'),
    path('remove-item/<pk>/', views.RemoveItemView.as_view(), name='remove'),
    path('checkout/', views.CheckoutView.as_view(success_url='cart:checkout'), name='checkout'),
]