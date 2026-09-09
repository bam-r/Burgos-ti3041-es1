from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista, name='lista'),
    path('producto/<int:producto_id>/', views.detalle, name='detalle'),
    path('comprar/<int:producto_id>/', views.comprar, name='comprar'),
]