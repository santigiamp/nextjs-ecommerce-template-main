from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import sqlite3
import json
from typing import List, Optional
import os
import shutil
import uuid
from pathlib import Path

app = FastAPI(title="E-commerce Mayorista API", version="2.0.0")

# Crear directorio para uploads si no existe
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Servir archivos estáticos (imágenes)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar dominios exactos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic mejorados
class Producto(BaseModel):
    id: int
    nombre: str
    precio: float
    descripcion: str
    imagen_url: str
    categoria: str
    stock: Optional[int] = None
    precio_mayorista: Optional[float] = None
    minimo_mayorista: Optional[int] = 1
    activo: bool = True

class ProductoCreate(BaseModel):
    nombre: str
    precio: float
    descripcion: str
    imagen_url: str
    categoria: str
    stock: Optional[int] = None
    precio_mayorista: Optional[float] = None
    minimo_mayorista: Optional[int] = 1
    activo: bool = True

class PedidoRequest(BaseModel):
    nombre: str
    telefono: str
    producto_id: int
    producto_nombre: str
    cantidad: int
    comentarios: Optional[str] = ""

class PedidoResponse(BaseModel):
    id: int
    mensaje: str

class ImageUploadResponse(BaseModel):
    filename: str
    url: str
    message: str

# Inicializar base de datos mejorada
def init_db():
    conn = sqlite3.connect('ecommerce.db')
    cursor = conn.cursor()
    
    # Crear tabla productos con campos adicionales
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            precio REAL NOT NULL,
            descripcion TEXT,
            imagen_url TEXT,
            categoria TEXT,
            stock INTEGER DEFAULT NULL,
            precio_mayorista REAL DEFAULT NULL,
            minimo_mayorista INTEGER DEFAULT 1,
            activo BOOLEAN DEFAULT 1,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Crear tabla pedidos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            telefono TEXT NOT NULL,
            producto_id INTEGER,
            producto_nombre TEXT,
            cantidad INTEGER,
            comentarios TEXT,
            fecha_pedido DATETIME DEFAULT CURRENT_TIMESTAMP,
            estado TEXT DEFAULT 'pendiente'
        )
    ''')
    
    # Verificar si hay productos, si no, insertar ejemplos
    cursor.execute('SELECT COUNT(*) FROM productos')
    if cursor.fetchone()[0] == 0:
        productos_ejemplo = [
            (
                "Gorro de Invierno Unicornio",
                2500.00,
                "Gorro térmico para niñas con diseño de unicornio. Tallas 2-8 años. Material: acrílico suave.",
                "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=400&fit=crop",
                "Gorros",
                50,  # stock
                2000.00,  # precio_mayorista
                5,  # minimo_mayorista
                1   # activo
            ),
            (
                "Gorro Polar Dinosaurio",
                2200.00,
                "Gorro polar con orejas de dinosaurio. Perfecto para niños aventureros. Tallas 3-10 años.",
                "https://images.unsplash.com/photo-1607083206869-4c7672e72a8a?w=400&h=400&fit=crop",
                "Gorros",
                30,
                1800.00,
                5,
                1
            ),
            (
                "Gorro Navideño Reno",
                1800.00,
                "Gorro festivo con diseño de reno navideño. Ideal para las fiestas. Talla única.",
                "https://images.unsplash.com/photo-1544473244-f6895e69ad8b?w=400&h=400&fit=crop",
                "Gorros",
                25,
                1400.00,
                10,
                1
            ),
            (
                "Gorro Térmico Oso Panda",
                2300.00,
                "Gorro de invierno súper suave con diseño de oso panda. Material hipoalergénico.",
                "https://images.unsplash.com/photo-1578761499019-d9d4b2a9c18e?w=400&h=400&fit=crop",
                "Gorros",
                40,
                1900.00,
                5,
                1
            ),
            (
                "Gorro Reversible Astronauta",
                2800.00,
                "Gorro reversible con diseño espacial. Un lado astronauta, otro lado galaxia. Novedad!",
                "https://images.unsplash.com/photo-1581833971358-2c8b550f87b3?w=400&h=400&fit=crop",
                "Gorros",
                15,
                2300.00,
                3,
                1
            )
        ]
        
        cursor.executemany(
            '''INSERT INTO productos 
               (nombre, precio, descripcion, imagen_url, categoria, stock, precio_mayorista, minimo_mayorista, activo) 
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            productos_ejemplo
        )
    
    conn.commit()
    conn.close()

# Inicializar DB al arrancar
init_db()

@app.get("/")
def read_root():
    return {
        "mensaje": "API E-commerce Mayorista v2.0 funcionando correctamente",
        "features": ["Upload de imágenes", "Gestión de stock", "Precios mayoristas"],
        "endpoints": ["/productos", "/pedidos", "/upload-image", "/docs"]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "2.0.0"}

@app.post("/upload-image", response_model=ImageUploadResponse)
async def upload_image(file: UploadFile = File(...)):
    """Subir imagen de producto"""
    try:
        # Asegurar que el directorio uploads existe
        UPLOAD_DIR.mkdir(exist_ok=True)
        
        # Validar tipo de archivo
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")
        
        # Validar que el archivo tenga nombre
        if not file.filename:
            raise HTTPException(status_code=400, detail="El archivo debe tener un nombre")
        
        # Generar nombre único
        file_extension = file.filename.split(".")[-1] if "." in file.filename else "jpg"
        unique_filename = f"{uuid.uuid4()}.{file_extension}"
        file_path = UPLOAD_DIR / unique_filename
        
        # Leer y guardar archivo
        content = await file.read()
        with file_path.open("wb") as buffer:
            buffer.write(content)
        
        # URL para acceder a la imagen
        image_url = f"/uploads/{unique_filename}"
        
        return ImageUploadResponse(
            filename=unique_filename,
            url=image_url,
            message="Imagen subida exitosamente"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = f"Error al subir imagen: {str(e)}. Traceback: {traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_detail)

@app.get("/productos", response_model=List[Producto])
def get_productos(categoria: Optional[str] = None, activo: bool = True):
    """Obtener productos con filtros opcionales"""
    try:
        conn = sqlite3.connect('ecommerce.db')
        cursor = conn.cursor()
        
        # Query base
        query = '''SELECT id, nombre, precio, descripcion, imagen_url, categoria, 
                          stock, precio_mayorista, minimo_mayorista, activo 
                   FROM productos WHERE activo = ?'''
        params = [activo]
        
        # Filtro por categoría
        if categoria:
            query += ' AND categoria = ?'
            params.append(categoria)
        
        query += ' ORDER BY id DESC'
        
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        productos = []
        for row in rows:
            productos.append(Producto(
                id=row[0],
                nombre=row[1],
                precio=row[2],
                descripcion=row[3],
                imagen_url=row[4],
                categoria=row[5],
                stock=row[6],
                precio_mayorista=row[7],
                minimo_mayorista=row[8] or 1,
                activo=bool(row[9])
            ))
        
        conn.close()
        return productos
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener productos: {str(e)}")

@app.get("/productos/{producto_id}", response_model=Producto)
def get_producto(producto_id: int):
    """Obtener un producto específico"""
    try:
        conn = sqlite3.connect('ecommerce.db')
        cursor = conn.cursor()
        
        cursor.execute('''SELECT id, nombre, precio, descripcion, imagen_url, categoria, 
                                 stock, precio_mayorista, minimo_mayorista, activo 
                          FROM productos WHERE id = ?''', (producto_id,))
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        producto = Producto(
            id=row[0],
            nombre=row[1],
            precio=row[2],
            descripcion=row[3],
            imagen_url=row[4],
            categoria=row[5],
            stock=row[6],
            precio_mayorista=row[7],
            minimo_mayorista=row[8] or 1,
            activo=bool(row[9])
        )
        
        conn.close()
        return producto
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener producto: {str(e)}")

@app.post("/productos", response_model=Producto)
def crear_producto(producto: ProductoCreate):
    """Crear nuevo producto"""
    try:
        conn = sqlite3.connect('ecommerce.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO productos (nombre, precio, descripcion, imagen_url, categoria, 
                                 stock, precio_mayorista, minimo_mayorista, activo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            producto.nombre,
            producto.precio,
            producto.descripcion,
            producto.imagen_url,
            producto.categoria,
            producto.stock,
            producto.precio_mayorista,
            producto.minimo_mayorista,
            producto.activo
        ))
        
        producto_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Retornar el producto creado
        return Producto(
            id=producto_id,
            **producto.dict()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear producto: {str(e)}")

@app.get("/categorias")
def get_categorias():
    """Obtener todas las categorías disponibles"""
    try:
        conn = sqlite3.connect('ecommerce.db')
        cursor = conn.cursor()
        
        cursor.execute('SELECT DISTINCT categoria FROM productos WHERE activo = 1 ORDER BY categoria')
        categorias = [row[0] for row in cursor.fetchall()]
        
        conn.close()
        return {"categorias": categorias}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener categorías: {str(e)}")

@app.post("/pedidos", response_model=PedidoResponse)
def crear_pedido(pedido: PedidoRequest):
    """Crear un nuevo pedido"""
    try:
        conn = sqlite3.connect('ecommerce.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO pedidos (nombre, telefono, producto_id, producto_nombre, cantidad, comentarios)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            pedido.nombre,
            pedido.telefono,
            pedido.producto_id,
            pedido.producto_nombre,
            pedido.cantidad,
            pedido.comentarios
        ))
        
        pedido_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return PedidoResponse(
            id=pedido_id,
            mensaje=f"Pedido #{pedido_id} registrado correctamente. Nos contactaremos pronto!"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear pedido: {str(e)}")

@app.get("/pedidos")
def get_pedidos():
    """Obtener todos los pedidos (para uso interno)"""
    try:
        conn = sqlite3.connect('ecommerce.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT id, nombre, telefono, producto_nombre, cantidad, comentarios, fecha_pedido, estado
            FROM pedidos ORDER BY fecha_pedido DESC
        ''')
        rows = cursor.fetchall()
        
        pedidos = []
        for row in rows:
            pedidos.append({
                "id": row[0],
                "nombre": row[1],
                "telefono": row[2],
                "producto_nombre": row[3],
                "cantidad": row[4],
                "comentarios": row[5],
                "fecha_pedido": row[6],
                "estado": row[7]
            })
        
        conn.close()
        return {"pedidos": pedidos}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener pedidos: {str(e)}")

@app.post("/actualizar-imagen-producto")
def actualizar_imagen_producto(producto_id: int, imagen_url: str):
    """Actualizar la URL de imagen de un producto (para uso interno)"""
    try:
        conn = sqlite3.connect('ecommerce.db')
        cursor = conn.cursor()
        
        cursor.execute(
            "UPDATE productos SET imagen_url = ? WHERE id = ?",
            (imagen_url, producto_id)
        )
        
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail=f"Producto con ID {producto_id} no encontrado")
        
        conn.commit()
        conn.close()
        
        return {"message": f"Imagen del producto {producto_id} actualizada exitosamente", "nueva_url": imagen_url}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar imagen: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)