#!/usr/bin/env python3
"""
Script para agregar los gorros que tenían imágenes válidas pero fueron eliminados
"""

import requests

# Configuración
API_URL = "https://nextjs-ecommerce-template-main-production.up.railway.app"

# Los 12 gorros que tenían imágenes válidas pero fueron eliminados
GORROS_FALTANTES = [
    {
        "nombre": "Gorro Violeta Moderno",
        "precio": 2500.0,
        "descripcion": "Gorro violeta de diseño moderno. Material premium y muy cómodo.",
        "imagen_url": "https://res.cloudinary.com/dakyybuuz/image/upload/v1751294000/gorros/producto_1751293999.861197.jpg"
    },
    {
        "nombre": "Gorro Turquesa Fresco", 
        "precio": 2400.0,
        "descripcion": "Gorro turquesa con acabado fresco. Perfecto para destacar con estilo.",
        "imagen_url": "https://res.cloudinary.com/dakyybuuz/image/upload/v1751294004/gorros/producto_1751294004.636279.jpg"
    },
    {
        "nombre": "Gorro Marrón Tierra",
        "precio": 2300.0,
        "descripcion": "Gorro en tono marrón tierra. Elegante y versátil para cualquier ocasión.",
        "imagen_url": "https://res.cloudinary.com/dakyybuuz/image/upload/v1751294009/gorros/producto_1751294009.497171.jpg"
    },
    {
        "nombre": "Gorro Beige Natural",
        "precio": 2450.0,
        "descripcion": "Gorro beige de color natural. Suave textura y gran comodidad.",
        "imagen_url": "https://res.cloudinary.com/dakyybuuz/image/upload/v1751294013/gorros/producto_1751294013.489298.jpg"
    },
    {
        "nombre": "Gorro Azul Marino",
        "precio": 2550.0,
        "descripcion": "Gorro azul marino clásico. Perfecto para un look sofisticado.",
        "imagen_url": "https://res.cloudinary.com/dakyybuuz/image/upload/v1751294017/gorros/producto_1751294017.662964.jpg"
    },
    {
        "nombre": "Gorro Verde Oliva",
        "precio": 2350.0,
        "descripcion": "Gorro verde oliva con estilo militar. Resistente y fashionable.",
        "imagen_url": "https://res.cloudinary.com/dakyybuuz/image/upload/v1751294023/gorros/producto_1751294023.297683.jpg"
    },
    {
        "nombre": "Gorro Burdeos Elegante",
        "precio": 2600.0,
        "descripcion": "Gorro burdeos de alta elegancia. Color profundo y textura premium.",
        "imagen_url": "https://res.cloudinary.com/dakyybuuz/image/upload/v1751294030/gorros/producto_1751294030.461909.jpg"
    },
    {
        "nombre": "Gorro Fucsia Atrevido",
        "precio": 2400.0,
        "descripcion": "Gorro fucsia para personalidades atrevidas. Color vibrante y llamativo.",
        "imagen_url": "https://res.cloudinary.com/dakyybuuz/image/upload/v1751294041/gorros/producto_1751294040.030185.jpg"
    },
    {
        "nombre": "Gorro Coral Primaveral",
        "precio": 2450.0,
        "descripcion": "Gorro coral con tonos primaverales. Fresco y juvenil.",
        "imagen_url": "https://res.cloudinary.com/dakyybuuz/image/upload/v1751294052/gorros/producto_1751294049.940031.jpg"
    },
    {
        "nombre": "Gorro Lavanda Delicado",
        "precio": 2300.0,
        "descripcion": "Gorro lavanda de tonalidad delicada. Suave al tacto y elegante.",
        "imagen_url": "https://res.cloudinary.com/dakyybuuz/image/upload/v1751294058/gorros/producto_1751294058.509544.jpg"
    },
    {
        "nombre": "Gorro Menta Refrescante",
        "precio": 2350.0,
        "descripcion": "Gorro menta con toque refrescante. Color único y moderno.",
        "imagen_url": "https://res.cloudinary.com/dakyybuuz/image/upload/v1751294063/gorros/producto_1751294063.341633.jpg"
    },
    {
        "nombre": "Gorro Salmón Suave",
        "precio": 2400.0,
        "descripcion": "Gorro salmón de textura suave. Perfecto para un look romántico.",
        "imagen_url": "https://res.cloudinary.com/dakyybuuz/image/upload/v1751294067/gorros/producto_1751294067.141568.jpg"
    }
]

def create_product(product_data):
    """Crear un nuevo producto"""
    try:
        full_product_data = {
            **product_data,
            "categoria": "Gorros",
            "stock": 50,
            "precio_mayorista": product_data['precio'] * 0.8,  # 20% descuento mayorista
            "minimo_mayorista": 5,
            "activo": True
        }
        
        response = requests.post(f"{API_URL}/productos", json=full_product_data)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error creando producto: {e}")
        return None

def get_current_products():
    """Obtener productos actuales"""
    try:
        response = requests.get(f"{API_URL}/productos")
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error obteniendo productos: {e}")
        return []

def main():
    """Función principal"""
    
    # Verificar conexión
    try:
        response = requests.get(f"{API_URL}/health")
        response.raise_for_status()
        print("✅ Conexión con Railway establecida")
    except:
        print("❌ No se puede conectar al backend de Railway")
        return
    
    # Mostrar productos actuales
    current_products = get_current_products()
    print(f"\n📋 Productos actuales: {len(current_products)}")
    
    # Agregar gorros faltantes
    print(f"\n🎨 Agregando {len(GORROS_FALTANTES)} gorros con imágenes válidas...")
    created_count = 0
    
    for gorro in GORROS_FALTANTES:
        result = create_product(gorro)
        if result:
            print(f"✅ Creado: {gorro['nombre']} (ID: {result['id']}) - ${gorro['precio']}")
            created_count += 1
        else:
            print(f"❌ Error creando: {gorro['nombre']}")
    
    print(f"\n🎉 Proceso completado!")
    print(f"📊 Gorros agregados: {created_count}")
    
    # Mostrar catálogo final
    final_products = get_current_products()
    print(f"\n📋 Catálogo final: {len(final_products)} productos")
    
    for i, product in enumerate(final_products, 1):
        print(f"{i:2}. {product['nombre']} - ${product['precio']}")

if __name__ == "__main__":
    main()