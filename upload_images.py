#!/usr/bin/env python3
"""
Script para subir imágenes de gorros a Cloudinary via backend y actualizar PostgreSQL.
Ejecutar este script después de colocar las imágenes de gorros en la carpeta 'gorros_images/'
"""

import os
import requests
from pathlib import Path

# Configuración
API_URL = "https://nextjs-ecommerce-template-main.onrender.com"  # URL de Render en producción
IMAGES_DIR = "gorros_images"  # Directorio con las imágenes de gorros

# Lista de nombres descriptivos para los gorros
GORROS_NOMBRES = [
    "Gorro Verde Premium",
    "Gorro Azul Especial", 
    "Gorro Rojo Clásico",
    "Gorro Negro Elegante",
    "Gorro Blanco Invernal",
    "Gorro Gris Urbano",
    "Gorro Rosa Suave",
    "Gorro Amarillo Vibrante",
    "Gorro Naranja Cálido",
    "Gorro Violeta Moderno",
    "Gorro Turquesa Fresco",
    "Gorro Marrón Tierra",
    "Gorro Beige Natural",
    "Gorro Azul Marino",
    "Gorro Verde Oliva",
    "Gorro Burdeos Elegante",
    "Gorro Fucsia Atrevido",
    "Gorro Coral Primaveral",
    "Gorro Lavanda Delicado",
    "Gorro Menta Refrescante",
    "Gorro Salmón Suave"
]

def upload_image(file_path):
    """Subir imagen al backend usando el endpoint /upload-image"""
    try:
        filename = os.path.basename(file_path)
        with open(file_path, 'rb') as file:
            files = {'file': (filename, file, 'image/jpeg')}
            response = requests.post(f"{API_URL}/upload-image", files=files, timeout=30)
            response.raise_for_status()
            return response.json()
    except Exception as e:
        print(f"Error subiendo {file_path}: {e}")
        return None

def create_product_with_image(nombre, image_url):
    """Crear un nuevo producto con imagen en PostgreSQL via API"""
    try:
        product_data = {
            "nombre": nombre,
            "precio": 2500.0,  # Precio base
            "descripcion": f"{nombre} de alta calidad. Material premium, muy cómodo y perfecto para el invierno.",
            "imagen_url": image_url,
            "categoria": "Gorros",
            "stock": 50,
            "precio_mayorista": 2000.0,
            "minimo_mayorista": 5,
            "activo": True
        }
        
        response = requests.post(f"{API_URL}/productos", json=product_data, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error creando producto {nombre}: {e}")
        return None

def main():
    """Función principal para subir todas las imágenes"""
    
    # Verificar que existe el directorio de imágenes
    if not os.path.exists(IMAGES_DIR):
        print(f"Creando directorio {IMAGES_DIR}/")
        os.makedirs(IMAGES_DIR)
        print(f"Por favor, coloca las 20 imágenes de gorros en {IMAGES_DIR}/ y ejecuta el script nuevamente.")
        return
    
    # Obtener lista de imágenes
    image_files = [f for f in os.listdir(IMAGES_DIR) 
                   if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))]
    
    if not image_files:
        print(f"No se encontraron imágenes en {IMAGES_DIR}/")
        print("Formatos soportados: .png, .jpg, .jpeg, .webp")
        return
    
    print(f"Encontradas {len(image_files)} imágenes")
    
    # Verificar conexión con el backend
    try:
        response = requests.get(f"{API_URL}/health")
        response.raise_for_status()
        print("✅ Conexión con backend establecida")
    except:
        print("❌ No se puede conectar al backend. Asegúrate de que esté ejecutándose.")
        print(f"URL configurada: {API_URL}")
        return
    
    # Subir imágenes y crear productos
    created_count = 0
    
    for i, image_file in enumerate(image_files[:21]):  # Máximo 21 imágenes
        file_path = os.path.join(IMAGES_DIR, image_file)
        print(f"\n[{i+1}/{len(image_files[:21])}] Subiendo {image_file}...")
        
        # Subir imagen a Cloudinary
        upload_result = upload_image(file_path)
        if upload_result:
            image_url = upload_result['url']  # Cloudinary ya devuelve la URL completa
            print(f"✅ Imagen subida a Cloudinary: {image_url}")
            
            # Crear producto con imagen
            if i < len(GORROS_NOMBRES):
                nombre_gorro = GORROS_NOMBRES[i]
                product_result = create_product_with_image(nombre_gorro, image_url)
                if product_result:
                    print(f"✅ Producto '{nombre_gorro}' creado con ID: {product_result['id']}")
                    created_count += 1
                else:
                    print(f"❌ Error creando producto '{nombre_gorro}'")
            else:
                print(f"⚠️  Imagen subida pero sin nombre asignado (índice {i})")
        else:
            print(f"❌ Error subiendo {image_file}")
    
    print(f"\n🎉 Proceso completado!")
    print(f"📊 Productos creados: {created_count}")
    print(f"🖼️  Imágenes procesadas: {len(image_files[:21])}")
    
    # Mostrar productos creados
    print("\n📋 Productos con imágenes de Cloudinary:")
    try:
        response = requests.get(f"{API_URL}/productos")
        response.raise_for_status()
        products = response.json()
        for product in products:
            if 'cloudinary' in product['imagen_url']:
                print(f"- {product['nombre']}: {product['imagen_url']}")
    except Exception as e:
        print(f"Error obteniendo productos: {e}")

if __name__ == "__main__":
    main()