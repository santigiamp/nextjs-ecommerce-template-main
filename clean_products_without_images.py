#!/usr/bin/env python3
"""
Script para eliminar productos que no tienen imágenes válidas de Cloudinary
"""

import requests

# Configuración
API_URL = "https://nextjs-ecommerce-template-main-production.up.railway.app"

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

def is_valid_cloudinary_image(image_url):
    """Verificar si la URL de imagen es válida de Cloudinary"""
    if not image_url:
        return False
    
    # URLs válidas de Cloudinary deben tener un timestamp/versión específico
    valid_patterns = [
        '/v1751293',  # URLs con timestamp específico generadas por el upload
        '/v1/gorros/producto_'  # URLs generadas recientemente
    ]
    
    return any(pattern in image_url for pattern in valid_patterns)

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
    
    # Obtener productos actuales
    print("\n📋 Analizando productos...")
    products = get_current_products()
    print(f"Total de productos: {len(products)}")
    
    # Clasificar productos
    valid_products = []
    invalid_products = []
    
    for product in products:
        image_url = product.get('imagen_url', '')
        if is_valid_cloudinary_image(image_url):
            valid_products.append(product)
        else:
            invalid_products.append(product)
    
    print(f"\n📊 Análisis:")
    print(f"✅ Productos con imágenes válidas: {len(valid_products)}")
    print(f"❌ Productos sin imágenes válidas: {len(invalid_products)}")
    
    # Mostrar productos que se van a eliminar
    if invalid_products:
        print(f"\n🗑️  Productos que se eliminarán:")
        for product in invalid_products:
            print(f"- ID {product['id']}: {product['nombre']}")
            print(f"  Imagen: {product.get('imagen_url', 'Sin imagen')}")
    
    # Confirmar eliminación
    if invalid_products:
        print(f"\n⚠️  Se eliminarán {len(invalid_products)} productos sin imágenes válidas.")
        
        # Eliminar productos sin imágenes válidas
        deleted_count = 0
        for product in invalid_products:
            if delete_product(product['id']):
                print(f"✅ Eliminado: {product['nombre']} (ID: {product['id']})")
                deleted_count += 1
            else:
                print(f"❌ Error eliminando: {product['nombre']} (ID: {product['id']})")
        
        print(f"\n🎉 Limpieza completada!")
        print(f"🗑️  Productos eliminados: {deleted_count}")
        print(f"✅ Productos conservados: {len(valid_products)}")
    else:
        print("\n✅ Todos los productos tienen imágenes válidas. No hay nada que limpiar.")
    
    # Mostrar productos finales
    print("\n📋 Productos finales:")
    final_products = get_current_products()
    print(f"Total: {len(final_products)} productos")
    
    for i, product in enumerate(final_products, 1):
        print(f"{i}. {product['nombre']} - ${product['precio']}")

if __name__ == "__main__":
    main()