import requests
from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import ProductForm
from django.conf import settings

API_URL = settings.API_URL

def lista_productos(request):
    response = requests.get(f'{API_URL}products/')
    productos = response.json()
    return render(request, 'productos/lista_productos.html', {'productos': productos})

def detalle_producto(request, product_id):
    response = requests.get(f'{API_URL}products/{product_id}')
    producto = response.json()
    return render(request, 'productos/detalle_producto.html', {'producto': producto})



def crear_producto(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            new_product = form.cleaned_data
            response = requests.post(f'{API_URL}products/create/', json=new_product)
            if response.status_code == 200:
                return redirect(reverse('lista_productos'))
    else:
        form = ProductForm()
    return render(request, 'productos/crear_producto.html', {'form': form})

def actualizar_producto(request, product_id):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            updated_product = form.cleaned_data
            requests.put(f'{API_URL}products/{product_id}', json=updated_product)
            return redirect(reverse('lista_productos'))
    else:
        response = requests.get(f'{API_URL}/{product_id}')
        product = response.json()
        form = ProductForm(initial=product)
    return render(request, 'productos/actualizar_producto.html', {'form': form, 'product_id': product_id})

def eliminar_producto(request, product_id):
    if request.method == 'POST':
        requests.delete(f'{API_URL}products/{product_id}')
        return redirect(reverse('lista_productos'))
    response = requests.get(f'{API_URL}products/{product_id}')
    producto = response.json()
    return render(request, 'productos/eliminar_producto.html', {'producto': producto})
