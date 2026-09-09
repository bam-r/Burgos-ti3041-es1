import json
from pathlib import Path

from django.http import Http404
from django.shortcuts import render, redirect

carrito = {}

# Ruta al archivo JSON con los datos del catálogo
DATA_PATH = Path(__file__).resolve().parent / 'data' / 'productos.json'


def cargar_productos():
    with open(DATA_PATH, encoding='utf-8') as archivo:
        productos=  json.load(archivo)
    for p in productos:
        p.setdefault('imagen', '/static/catalogo/img/sin-imagen.jpg')
    return productos

def guardar_productos(productos):
    with open(DATA_PATH, 'w', encoding='utf-8') as archivo:
        json.dump(productos, archivo, ensure_ascii=False, indent=2)

def obtener_carrito(productos):
    items = []
    for producto_id, cantidad in carrito.items():
        producto = next((p for p in productos if p['id'] == producto_id), None)
        if producto:
            items.append({'producto': producto, 'cantidad': cantidad})
    return items
        
def lista(request):
    productos = cargar_productos()

    total_productos = len(productos)
    disponibles = sum(1 for p in productos if p['stock'] > 0)

    resumen = {
        'total': total_productos,
        'disponibles': disponibles,
        'sin_stock': total_productos - disponibles,
    }

    contexto = {
        'productos': productos,
        'resumen': resumen,
        'carrito': obtener_carrito(productos),
    }
    return render(request, 'catalogo/lista.html', contexto)


def detalle(request, producto_id):
    productos = cargar_productos()
    producto = next((p for p in productos if p['id'] == producto_id), None)

    if producto is None:
        raise Http404("El producto solicitado no existe en el catálogo.")

    return render(request, 'catalogo/detalle.html', {'producto': producto})

def comprar(request, producto_id):
    productos = cargar_productos()
    producto = next((p for p in productos if p['id'] == producto_id), None)

    if producto is None:
        raise Http404("El producto solicitado no existe en el catálogo.")

    if request.method == 'POST' and producto['stock'] > 0:
        producto['stock'] -= 1
        guardar_productos(productos)
        carrito[producto_id] = carrito.get(producto_id, 0) + 1

    return redirect(request.META.get('HTTP_REFERER', 'lista'))