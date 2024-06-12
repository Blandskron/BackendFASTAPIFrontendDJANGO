import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
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
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            name = form.cleaned_data['name']
            price = form.cleaned_data['price']
            description = form.cleaned_data['description']
            image = request.FILES.get('image')

            image_url = None

            if image:
                try:
                    upload_url = f'{API_URL}uploadfile/'
                    files = {'file': (image.name, image.read(), image.content_type)}
                    response = requests.post(upload_url, files=files)
                    if response.status_code == 200:
                        image_url = response.json().get("file_path")
                        print("URL de la imagen subida:", image_url)
                    else:
                        error_message = f"Error al subir la imagen: {response.text}"
                        return render(request, 'error.html', {'message': error_message})
                except AttributeError as e:
                    print("Error al obtener atributos de la imagen:", e)
                    return render(request, 'error.html', {'message': 'Error al procesar la imagen. Verifique el archivo e intente nuevamente.'})
            
            if image_url:
                create_url = f'{API_URL}products/create/'
                product_data = {
                    "name": name,
                    "price": price,
                    "description": description,
                    "image_url": image_url
                }
                response = requests.post(create_url, json=product_data)
                if response.status_code == 200:
                    return redirect('lista_productos')
                else:
                    error_message = f"Error al crear el producto: {response.text}"
                    return render(request, 'error.html', {'message': error_message})
        else:
            print("Formulario no válido:", form.errors)
    else:
        form = ProductForm()

    return render(request, 'productos/crear_producto.html', {'form': form})

def actualizar_producto(request, product_id):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            updated_product = form.cleaned_data
            response = requests.put(f'{API_URL}products/{product_id}', json=updated_product)
            if response.status_code == 200:
                return redirect(reverse('lista_productos'))
            else:
                error_message = f"Error al actualizar el producto: {response.text}"
                return render(request, 'error.html', {'message': error_message})
    else:
        response = requests.get(f'{API_URL}products/{product_id}')
        product = response.json()
        form = ProductForm(initial=product)
    return render(request, 'productos/actualizar_producto.html', {'form': form, 'product_id': product_id})

def eliminar_producto(request, product_id):
    if request.method == 'POST':
        response = requests.delete(f'{API_URL}products/{product_id}')
        if response.status_code == 200:
            return redirect(reverse('lista_productos'))
        else:
            error_message = f"Error al eliminar el producto: {response.text}"
            return render(request, 'error.html', {'message': error_message})
    response = requests.get(f'{API_URL}products/{product_id}')
    producto = response.json()
    return render(request, 'productos/eliminar_producto.html', {'producto': producto})
