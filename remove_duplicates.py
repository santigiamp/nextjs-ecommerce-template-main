#!/usr/bin/env python3
"""
Script para eliminar productos duplicados
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
    print("\n📋 Analizando productos duplicados...")
    products = get_current_products()
    print(f"Total de productos: {len(products)}")
    
    # Buscar duplicados por nombre
    seen_names = {}
    duplicates = []
    
    for product in products:
        name = product['nombre']
        if name in seen_names:
            # Es un duplicado, mantener el ID menor (más antiguo)
            existing_product = seen_names[name]
            if product['id'] < existing_product['id']:
                # El actual es más antiguo, marcar el anterior como duplicado
                duplicates.append(existing_product)
                seen_names[name] = product
            else:
                # El anterior es más antiguo, marcar el actual como duplicado
                duplicates.append(product)
        else:
            seen_names[name] = product
    
    # Mostrar duplicados encontrados
    print(f"\n📊 Análisis:")
    print(f"✅ Productos únicos: {len(seen_names)}")
    print(f"❌ Productos duplicados a eliminar: {len(duplicates)}")
    
    if duplicates:
        print(f"\n🗑️  Productos duplicados que se eliminarán:")
        for product in duplicates:
            print(f"- ID {product['id']}: {product['nombre']}")
        
        # Eliminar duplicados
        deleted_count = 0
        for product in duplicates:
            if delete_product(product['id']):
                print(f"✅ Eliminado duplicado: {product['nombre']} (ID: {product['id']})")
                deleted_count += 1
            else:
                print(f"❌ Error eliminando: {product['nombre']} (ID: {product['id']})")
        
        print(f"\n🎉 Limpieza de duplicados completada!")
        print(f"🗑️  Duplicados eliminados: {deleted_count}")
    else:
        print("\n✅ No se encontraron productos duplicados.")
    
    # Mostrar productos finales
    print("\n📋 Productos finales:")
    final_products = get_current_products()
    print(f"Total: {len(final_products)} productos únicos")
    
    for i, product in enumerate(final_products, 1):
        print(f"{i}. {product['nombre']} - ${product['precio']} (ID: {product['id']})")

if __name__ == "__main__":
    main()