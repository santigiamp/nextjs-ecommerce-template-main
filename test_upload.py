#!/usr/bin/env python3
import requests
import os

API_URL = "https://nextjs-ecommerce-template-main.onrender.com"

def test_upload():
    print("🔍 Probando upload de imagen...")
    
    # Verificar conexión
    try:
        response = requests.get(f"{API_URL}/health", timeout=10)
        print(f"✅ Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"❌ Error en health check: {e}")
        return
    
    # Probar upload con la primera imagen
    images = [f for f in os.listdir("gorros_images") if f.lower().endswith(('.jpeg', '.jpg', '.png'))]
    if not images:
        print("❌ No se encontraron imágenes")
        return
    
    first_image = images[0]
    image_path = os.path.join("gorros_images", first_image)
    
    print(f"📸 Probando upload de: {first_image}")
    print(f"📏 Tamaño: {os.path.getsize(image_path) / 1024 / 1024:.2f} MB")
    
    try:
        with open(image_path, 'rb') as file:
            files = {'file': (first_image, file, 'image/jpeg')}
            response = requests.post(f"{API_URL}/upload-image", files=files, timeout=30)
            
        print(f"📊 Status Code: {response.status_code}")
        print(f"📄 Response: {response.text[:500]}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Upload exitoso: {result.get('url', 'No URL')}")
        else:
            print(f"❌ Upload falló: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error en upload: {e}")

if __name__ == "__main__":
    test_upload()