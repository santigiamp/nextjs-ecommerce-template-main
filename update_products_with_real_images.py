#!/usr/bin/env python3
"""
Script para actualizar los productos existentes con imágenes reales de Cloudinary
"""

import requests
import json

# Configuración
API_URL = "https://nextjs-ecommerce-template-main-production.up.railway.app"

# Las URLs de Cloudinary de sus gorros reales (asumiendo que ya están subidas)
# Formato: https://res.cloudinary.com/dakyybuuz/image/upload/v1/gorros/nombre_archivo
CLOUDINARY_BASE = "https://res.cloudinary.com/dakyybuuz/image/upload/v1/gorros/"

# Lista de gorros reales disponibles
GORROS_REALES = [
    {
        "nombre": "Gorro Tejido Artesanal Verde",
        "precio": 2500.0,
        "descripcion": "Gorro tejido a mano de alta calidad. Material premium, muy cómodo y perfecto para el invierno.",
        "imagen_filename": "WhatsApp_Image_2025-06-25_at_12.58.44"  # Sin extensión
    },
    {
        "nombre": "Gorro Tejido Artesanal Azul", 
        "precio": 2400.0,
        "descripcion": "Gorro tejido con diseño único. Perfecto para el clima frío con estilo moderno.",
        "imagen_filename": "WhatsApp_Image_2025-06-25_at_12.58.45"
    },
    {
        "nombre": "Gorro Tejido Premium Multicolor",
        "precio": 2600.0, 
        "descripcion": "Gorro tejido con patrón multicolor. Diseño exclusivo y material de primera calidad.",
        "imagen_filename": "WhatsApp_Image_2025-06-25_at_12.58.45_1"
    },
    {
        "nombre": "Gorro Tejido Clásico Gris",
        "precio": 2300.0,
        "descripcion": "Gorro tejido clásico en tono gris. Elegante y versátil para cualquier outfit.",
        "imagen_filename": "WhatsApp_Image_2025-06-25_at_12.58.45_2"
    },
    {
        "nombre": "Gorro Tejido Invernal Beige",
        "precio": 2500.0,
        "descripcion": "Gorro tejido en tono beige natural. Ideal para el invierno con acabado suave.",
        "imagen_filename": "WhatsApp_Image_2025-06-25_at_12.58.46"
    }
]

def get_current_products():
    """Obtener productos actuales"""
    try:
        response = requests.get(f"{API_URL}/productos")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error obteniendo productos: {e}")
        return []

def delete_product(product_id):
    """Eliminar un producto"""
    try:
        response = requests.delete(f"{API_URL}/productos/{product_id}")
        return response.status_code == 200
    except Exception as e:
        print(f"Error eliminando producto {product_id}: {e}")
        return False

def create_product(product_data):
    """Crear un nuevo producto"""
    try:
        response = requests.post(f"{API_URL}/productos", json=product_data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error creando producto: {e}")
        return None

def main():
    """Función principal"""
    
    # Verificar conexión con el backend
    try:
        response = requests.get(f"{API_URL}/health")
        response.raise_for_status()
        print("✅ Conexión con Railway establecida")
    except:
        print("❌ No se puede conectar al backend de Railway")
        return
    
    # Obtener productos actuales
    print("\n📋 Obteniendo productos actuales...")
    current_products = get_current_products()
    print(f"Encontrados {len(current_products)} productos")
    
    # Eliminar productos de ejemplo existentes
    print("\n🧹 Eliminando productos de ejemplo...")
    for product in current_products:
        if 'sample_gorros' in product.get('imagen_url', ''):
            if delete_product(product['id']):
                print(f"✅ Eliminado: {product['nombre']}")
            else:
                print(f"❌ Error eliminando: {product['nombre']}")
    
    # Crear productos con gorros reales
    print("\n🎨 Creando productos con gorros reales...")
    created_count = 0
    
    for gorro in GORROS_REALES:
        # Construir URL de Cloudinary
        imagen_url = f"{CLOUDINARY_BASE}{gorro['imagen_filename']}"
        
        product_data = {
            "nombre": gorro['nombre'],
            "precio": gorro['precio'],
            "descripcion": gorro['descripcion'],
            "imagen_url": imagen_url,
            "categoria": "Gorros",
            "stock": 50,
            "precio_mayorista": gorro['precio'] * 0.8,  # 20% descuento mayorista
            "minimo_mayorista": 5,
            "activo": True
        }
        
        result = create_product(product_data)
        if result:
            print(f"✅ Creado: {gorro['nombre']} (ID: {result['id']})")
            created_count += 1
        else:
            print(f"❌ Error creando: {gorro['nombre']}")
    
    print(f"\n🎉 Proceso completado!")
    print(f"📊 Productos creados: {created_count}")
    
    # Mostrar productos finales
    print("\n📋 Productos actuales:")
    final_products = get_current_products()
    for product in final_products:
        print(f"- {product['nombre']}: ${product['precio']}")
        print(f"  Imagen: {product['imagen_url']}")

if __name__ == "__main__":
    main()