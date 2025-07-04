from fastapi import FastAPI, HTTPException, UploadFile, File, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
try:
    from pydantic import EmailStr
except ImportError:
    EmailStr = str
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean, DateTime, Text
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.sql import func
import cloudinary
import cloudinary.uploader
import json
from typing import List, Optional
import os
from datetime import datetime
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from jinja2 import Template

app = FastAPI(title="E-commerce Mayorista API", version="3.0.0")

# Configuración de PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("Warning: DATABASE_URL not found, using SQLite fallback")
    DATABASE_URL = "sqlite:///./ecommerce.db"
else:
    print(f"DATABASE_URL configured: {DATABASE_URL is not None}")
    print(f"DATABASE_URL starts with: {DATABASE_URL[:20]}...")

# Usar driver psycopg2 estándar
# No necesitamos modificar la URL para psycopg2

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Configuración de Cloudinary
cloudinary_name = os.getenv("CLOUDINARY_CLOUD_NAME")
cloudinary_key = os.getenv("CLOUDINARY_API_KEY")
cloudinary_secret = os.getenv("CLOUDINARY_API_SECRET")

if not all([cloudinary_name, cloudinary_key, cloudinary_secret]):
    print("Warning: Cloudinary not configured, image uploads will be disabled")
    cloudinary_name = None

print(f"Cloudinary configured: name={cloudinary_name is not None}, key={cloudinary_key is not None}, secret={cloudinary_secret is not None}")

if cloudinary_name:
    cloudinary.config(
        cloud_name=cloudinary_name,
        api_key=cloudinary_key,
        api_secret=cloudinary_secret
    )

# Configuración de Email
MAIL_USERNAME = os.getenv("MAIL_USERNAME")
MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
MAIL_FROM = os.getenv("MAIL_FROM")

if not all([MAIL_USERNAME, MAIL_PASSWORD, MAIL_FROM]):
    print("Warning: Email not configured, email notifications will be disabled")
    MAIL_USERNAME = None

MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587

# Modelo de la base de datos
class ProductoDB(Base):
    __tablename__ = "productos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    precio = Column(Float, nullable=False)
    descripcion = Column(Text)
    imagen_url = Column(String)
    categoria = Column(String)
    stock = Column(Integer)
    precio_mayorista = Column(Float)
    minimo_mayorista = Column(Integer, default=1)
    activo = Column(Boolean, default=True)
    fecha_creacion = Column(DateTime, default=func.now())

class PedidoDB(Base):
    __tablename__ = "pedidos"
    
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    email = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    producto_id = Column(Integer)
    producto_nombre = Column(String)
    cantidad = Column(Integer)
    comentarios = Column(Text)
    fecha_pedido = Column(DateTime, default=func.now())
    estado = Column(String, default="pendiente")

# Crear tablas
Base.metadata.create_all(bind=engine)

# Dependency para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("ALLOWED_ORIGINS", "").split(",") if os.getenv("ALLOWED_ORIGINS") else ["*"],
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
    email: str  # No usamos EmailStr para evitar dependencias
    telefono: str
    producto_id: int
    producto_nombre: str
    cantidad: int
    comentarios: Optional[str] = ""
    email_destino: Optional[str] = None  # Email adicional del frontend

class PedidoResponse(BaseModel):
    id: int
    mensaje: str

class ImageUploadResponse(BaseModel):
    filename: str
    url: str
    message: str

# Función para inicializar productos de ejemplo
def init_sample_products():
    db = SessionLocal()
    try:
        # Verificar si hay productos
        count = db.query(ProductoDB).count()
        if count == 0:
            productos_ejemplo = [
                ProductoDB(
                    nombre="Gorro Verde Premium",
                    precio=2500.00,
                    descripcion="Gorro de alta calidad en color verde. Material premium, muy cómodo.",
                    imagen_url="https://res.cloudinary.com/dakyybuuz/image/upload/v1/sample_gorros/gorro_verde",
                    categoria="Gorros",
                    stock=50,
                    precio_mayorista=2000.00,
                    minimo_mayorista=5,
                    activo=True
                ),
                ProductoDB(
                    nombre="Gorro Azul Especial",
                    precio=2200.00,
                    descripcion="Gorro azul de diseño especial. Perfecto para el invierno.",
                    imagen_url="https://res.cloudinary.com/dakyybuuz/image/upload/v1/sample_gorros/gorro_azul",
                    categoria="Gorros",
                    stock=30,
                    precio_mayorista=1800.00,
                    minimo_mayorista=5,
                    activo=True
                )
            ]
            
            for producto in productos_ejemplo:
                db.add(producto)
            db.commit()
    finally:
        db.close()

# Inicializar productos de ejemplo al arrancar
init_sample_products()

# Función para enviar email de notificación
async def send_order_email(pedido: PedidoRequest, pedido_id: int):
    """Enviar email de confirmación de pedido"""
    try:
        # Template para el email
        email_template = """
        <html>
        <body style="font-family: Arial, sans-serif; background-color: #f9f9f9; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #f97316; margin: 0;">🛒 Nuevo Pedido - Distribuidora Alegría</h1>
                    <p style="color: #666; margin: 10px 0;">🌈 Mayorista de Juguetes 🎨</p>
                </div>
                
                <div style="background: linear-gradient(135deg, #fed7aa 0%, #fef3c7 100%); padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                    <h2 style="color: #1f2937; margin: 0 0 15px 0;">📦 Detalles del Pedido #{{ pedido_id }}</h2>
                    <p style="margin: 5px 0;"><strong>📅 Fecha:</strong> {{ fecha }}</p>
                </div>
                
                <div style="background-color: #f0fdf4; border-left: 4px solid #22c55e; padding: 20px; margin-bottom: 20px;">
                    <h3 style="color: #15803d; margin: 0 0 15px 0;">👤 Información del Cliente</h3>
                    <p style="margin: 5px 0;"><strong>Nombre:</strong> {{ nombre }}</p>
                    <p style="margin: 5px 0;"><strong>Email:</strong> {{ email }}</p>
                    <p style="margin: 5px 0;"><strong>Teléfono:</strong> {{ telefono }}</p>
                </div>
                
                <div style="background-color: #eff6ff; border-left: 4px solid #3b82f6; padding: 20px; margin-bottom: 20px;">
                    <h3 style="color: #1d4ed8; margin: 0 0 15px 0;">🎁 Producto Solicitado</h3>
                    <p style="margin: 5px 0;"><strong>Producto:</strong> {{ producto_nombre }}</p>
                    <p style="margin: 5px 0;"><strong>Cantidad:</strong> {{ cantidad }} unidades</p>
                    {% if comentarios %}
                    <p style="margin: 15px 0 5px 0;"><strong>Comentarios:</strong></p>
                    <p style="background-color: #f8fafc; padding: 10px; border-radius: 5px; margin: 5px 0;">{{ comentarios }}</p>
                    {% endif %}
                </div>
                
                <div style="background-color: #fef3c7; border: 1px solid #f59e0b; padding: 15px; border-radius: 8px; margin: 20px 0;">
                    <p style="margin: 0; color: #92400e; font-weight: bold;">⚡ Acción requerida:</p>
                    <p style="margin: 5px 0; color: #92400e;">Contactar al cliente lo antes posible para confirmar disponibilidad y coordinar entrega.</p>
                </div>
                
                <div style="text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #e5e7eb;">
                    <p style="color: #6b7280; font-size: 14px; margin: 0;">Distribuidora Alegría - Mayorista de Juguetes</p>
                    <p style="color: #6b7280; font-size: 12px; margin: 5px 0 0 0;">Este email fue generado automáticamente desde el sistema de pedidos</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Renderizar template
        template = Template(email_template)
        html_content = template.render(
            pedido_id=pedido_id,
            fecha=datetime.now().strftime("%d/%m/%Y %H:%M"),
            nombre=pedido.nombre,
            email=pedido.email,
            telefono=pedido.telefono,
            producto_nombre=pedido.producto_nombre,
            cantidad=pedido.cantidad,
            comentarios=pedido.comentarios
        )
        
        # Determinar email de destino
        email_destino = pedido.email_destino or os.getenv("DEFAULT_EMAIL_RECIPIENT")
        
        # Crear mensaje
        message = MIMEMultipart("alternative")
        message["Subject"] = f"🛒 Nuevo Pedido #{pedido_id} - {pedido.producto_nombre}"
        message["From"] = MAIL_FROM
        message["To"] = email_destino
        
        # Crear parte HTML
        html_part = MIMEText(html_content, "html")
        message.attach(html_part)
        
        # Enviar email
        await aiosmtplib.send(
            message,
            hostname=MAIL_SERVER,
            port=MAIL_PORT,
            start_tls=True,
            username=MAIL_USERNAME,
            password=MAIL_PASSWORD,
        )
        
        print(f"Email enviado exitosamente para pedido #{pedido_id} a {email_destino}")
        
    except Exception as e:
        print(f"Error al enviar email: {str(e)}")
        # No lanzamos excepción para que el pedido se registre aunque falle el email

@app.get("/")
def read_root():
    return {
        "mensaje": "API E-commerce Mayorista v3.0 funcionando correctamente",
        "features": ["PostgreSQL", "Cloudinary", "Upload de imágenes", "Gestión de stock", "Precios mayoristas"],
        "endpoints": ["/productos", "/pedidos", "/upload-image", "/docs"]
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "version": "3.0.0", "database": "PostgreSQL", "storage": "Cloudinary"}

@app.post("/upload-image", response_model=ImageUploadResponse)
async def upload_image(file: UploadFile = File(...)):
    """Subir imagen de producto a Cloudinary"""
    try:
        if not cloudinary_name:
            raise HTTPException(status_code=503, detail="Image upload service not configured")
            
        # Validar tipo de archivo
        if not file.content_type.startswith("image/"):
            raise HTTPException(status_code=400, detail="El archivo debe ser una imagen")
        
        # Validar que el archivo tenga nombre
        if not file.filename:
            raise HTTPException(status_code=400, detail="El archivo debe tener un nombre")
        
        # Leer el contenido del archivo
        content = await file.read()
        
        # Subir a Cloudinary
        upload_result = cloudinary.uploader.upload(
            content,
            folder="gorros",
            public_id=f"producto_{datetime.now().timestamp()}",
            overwrite=True,
            resource_type="image"
        )
        
        return ImageUploadResponse(
            filename=upload_result["public_id"],
            url=upload_result["secure_url"],
            message="Imagen subida exitosamente a Cloudinary"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        import traceback
        error_detail = f"Error al subir imagen: {str(e)}. Traceback: {traceback.format_exc()}"
        raise HTTPException(status_code=500, detail=error_detail)

@app.get("/productos", response_model=List[Producto])
def get_productos(categoria: Optional[str] = None, activo: bool = True, db: Session = Depends(get_db)):
    """Obtener productos con filtros opcionales"""
    try:
        # Query base
        query = db.query(ProductoDB).filter(ProductoDB.activo == activo)
        
        # Filtro por categoría
        if categoria:
            query = query.filter(ProductoDB.categoria == categoria)
        
        query = query.order_by(ProductoDB.id.desc())
        
        productos_db = query.all()
        
        productos = []
        for producto_db in productos_db:
            productos.append(Producto(
                id=producto_db.id,
                nombre=producto_db.nombre,
                precio=producto_db.precio,
                descripcion=producto_db.descripcion,
                imagen_url=producto_db.imagen_url,
                categoria=producto_db.categoria,
                stock=producto_db.stock,
                precio_mayorista=producto_db.precio_mayorista,
                minimo_mayorista=producto_db.minimo_mayorista or 1,
                activo=producto_db.activo
            ))
        
        return productos
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener productos: {str(e)}")

@app.get("/productos/{producto_id}", response_model=Producto)
def get_producto(producto_id: int, db: Session = Depends(get_db)):
    """Obtener un producto específico"""
    try:
        producto_db = db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()
        
        if not producto_db:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        
        producto = Producto(
            id=producto_db.id,
            nombre=producto_db.nombre,
            precio=producto_db.precio,
            descripcion=producto_db.descripcion,
            imagen_url=producto_db.imagen_url,
            categoria=producto_db.categoria,
            stock=producto_db.stock,
            precio_mayorista=producto_db.precio_mayorista,
            minimo_mayorista=producto_db.minimo_mayorista or 1,
            activo=producto_db.activo
        )
        
        return producto
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener producto: {str(e)}")

@app.post("/productos", response_model=Producto)
def crear_producto(producto: ProductoCreate, db: Session = Depends(get_db)):
    """Crear nuevo producto"""
    try:
        producto_db = ProductoDB(
            nombre=producto.nombre,
            precio=producto.precio,
            descripcion=producto.descripcion,
            imagen_url=producto.imagen_url,
            categoria=producto.categoria,
            stock=producto.stock,
            precio_mayorista=producto.precio_mayorista,
            minimo_mayorista=producto.minimo_mayorista,
            activo=producto.activo
        )
        
        db.add(producto_db)
        db.commit()
        db.refresh(producto_db)
        
        # Retornar el producto creado
        return Producto(
            id=producto_db.id,
            **producto.dict()
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear producto: {str(e)}")

@app.get("/categorias")
def get_categorias(db: Session = Depends(get_db)):
    """Obtener todas las categorías disponibles"""
    try:
        categorias_result = db.query(ProductoDB.categoria).filter(ProductoDB.activo == True).distinct().order_by(ProductoDB.categoria).all()
        categorias = [categoria[0] for categoria in categorias_result if categoria[0]]
        
        return {"categorias": categorias}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener categorías: {str(e)}")

@app.post("/pedidos", response_model=PedidoResponse)
async def crear_pedido(pedido: PedidoRequest, background_tasks: BackgroundTasks, db: Session = Depends(get_db)):
    """Crear un nuevo pedido y enviar notificación por email"""
    try:
        pedido_db = PedidoDB(
            nombre=pedido.nombre,
            email=pedido.email,
            telefono=pedido.telefono,
            producto_id=pedido.producto_id,
            producto_nombre=pedido.producto_nombre,
            cantidad=pedido.cantidad,
            comentarios=pedido.comentarios
        )
        
        db.add(pedido_db)
        db.commit()
        db.refresh(pedido_db)
        
        # Enviar email en background solo si está configurado
        if MAIL_USERNAME:
            background_tasks.add_task(send_order_email, pedido, pedido_db.id)
        
        return PedidoResponse(
            id=pedido_db.id,
            mensaje=f"Pedido #{pedido_db.id} registrado correctamente. Se ha enviado una notificación por email."
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al crear pedido: {str(e)}")

@app.get("/pedidos")
def get_pedidos(db: Session = Depends(get_db)):
    """Obtener todos los pedidos (para uso interno)"""
    try:
        pedidos_db = db.query(PedidoDB).order_by(PedidoDB.fecha_pedido.desc()).all()
        
        pedidos = []
        for pedido_db in pedidos_db:
            pedidos.append({
                "id": pedido_db.id,
                "nombre": pedido_db.nombre,
                "email": getattr(pedido_db, 'email', ''),  # Compatibilidad con pedidos antiguos
                "telefono": pedido_db.telefono,
                "producto_nombre": pedido_db.producto_nombre,
                "cantidad": pedido_db.cantidad,
                "comentarios": pedido_db.comentarios,
                "fecha_pedido": pedido_db.fecha_pedido.isoformat() if pedido_db.fecha_pedido else None,
                "estado": pedido_db.estado
            })
        
        return {"pedidos": pedidos}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener pedidos: {str(e)}")

@app.post("/actualizar-imagen-producto")
def actualizar_imagen_producto(producto_id: int, imagen_url: str, db: Session = Depends(get_db)):
    """Actualizar la URL de imagen de un producto (para uso interno)"""
    try:
        producto_db = db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()
        
        if not producto_db:
            raise HTTPException(status_code=404, detail=f"Producto con ID {producto_id} no encontrado")
        
        producto_db.imagen_url = imagen_url
        db.commit()
        
        return {"message": f"Imagen del producto {producto_id} actualizada exitosamente", "nueva_url": imagen_url}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al actualizar imagen: {str(e)}")

@app.delete("/productos/{producto_id}")
def eliminar_producto(producto_id: int, db: Session = Depends(get_db)):
    """Eliminar un producto por ID"""
    try:
        # Verificar si el producto existe
        producto_db = db.query(ProductoDB).filter(ProductoDB.id == producto_id).first()
        
        if not producto_db:
            raise HTTPException(status_code=404, detail=f"Producto con ID {producto_id} no encontrado")
        
        # Eliminar el producto
        db.delete(producto_db)
        db.commit()
        
        return {"message": f"Producto {producto_id} eliminado exitosamente"}
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al eliminar producto: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8080"))
    print(f"Starting server on port {port}")
    uvicorn.run(app, host="0.0.0.0", port=port)