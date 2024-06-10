from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_productos, name='lista_productos'),
    path('<int:product_id>/', views.detalle_producto, name='detalle_producto'),
    path('crear/', views.crear_producto, name='crear_producto'),
    path('actualizar/<int:product_id>/', views.actualizar_producto, name='actualizar_producto'),
    path('eliminar/<int:product_id>/', views.eliminar_producto, name='eliminar_producto'),
]
