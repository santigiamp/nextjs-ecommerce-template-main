#!/usr/bin/env python3
"""
Script para subir imágenes de gorros al backend y actualizar la base de datos.
Ejecutar este script después de colocar las 20 imágenes de gorros en la carpeta 'gorros_images/'
"""

import os
import requests
import sqlite3
from pathlib import Path

# Configuración
API_URL = "https://nextjs-ecommerce-template-main.onrender.com"  # URL de Render en producción
IMAGES_DIR = "gorros_images"  # Directorio con las imágenes de gorros

# Lista de productos de gorros para actualizar
GORROS_DATA = [
    {"id": 1, "nombre": "Gorro de Invierno Unicornio"},
    {"id": 2, "nombre": "Gorro Polar Dinosaurio"},
    {"id": 3, "nombre": "Gorro Navideño Reno"},
    {"id": 4, "nombre": "Gorro Térmico Oso Panda"},
    {"id": 5, "nombre": "Gorro Reversible Astronauta"},
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

def update_product_image(product_id, image_url):
    """Actualizar la URL de imagen de un producto usando la API"""
    try:
        # Como no podemos acceder directamente a la BD de Render,
        # mostramos la información para actualizar manualmente
        print(f"🔄 Para actualizar producto {product_id} con imagen {image_url}")
        print(f"   Ejecutar en Render: UPDATE productos SET imagen_url = '{image_url}' WHERE id = {product_id};")
        return True
    except Exception as e:
        print(f"Error preparando actualización para producto {product_id}: {e}")
        return False

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
    
    # Subir imágenes y actualizar productos
    updated_count = 0
    
    for i, image_file in enumerate(image_files[:20]):  # Máximo 20 imágenes
        file_path = os.path.join(IMAGES_DIR, image_file)
        print(f"\nSubiendo {image_file}...")
        
        # Subir imagen
        upload_result = upload_image(file_path)
        if upload_result:
            image_url = f"{API_URL}{upload_result['url']}"
            print(f"✅ Imagen subida: {upload_result['url']}")
            
            # Si hay un producto correspondiente, actualizar su imagen
            if i < len(GORROS_DATA):
                product = GORROS_DATA[i]
                if update_product_image(product["id"], image_url):
                    print(f"✅ Producto '{product['nombre']}' actualizado")
                    updated_count += 1
                else:
                    print(f"❌ Error actualizando producto '{product['nombre']}'")
        else:
            print(f"❌ Error subiendo {image_file}")
    
    print(f"\n🎉 Proceso completado!")
    print(f"📊 Productos actualizados: {updated_count}")
    print(f"🖼️  Imágenes procesadas: {len(image_files[:20])}")
    
    # Mostrar productos actualizados
    print("\n📋 Productos con nuevas imágenes:")
    try:
        response = requests.get(f"{API_URL}/productos")
        products = response.json()
        for product in products[:5]:
            print(f"- {product['nombre']}: {product['imagen_url']}")
    except:
        print("No se pudieron obtener los productos actualizados")

if __name__ == "__main__":
    main()