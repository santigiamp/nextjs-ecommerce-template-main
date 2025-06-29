# E-commerce de Juguetes y Ropa Infantil

Un e-commerce completo para productos infantiles con backend en FastAPI y frontend en Next.js.

## 🏗️ Arquitectura

### Backend (FastAPI)
- **Framework**: FastAPI
- **Base de datos**: SQLite
- **Funcionalidades**:
  - API REST para productos
  - Gestión de pedidos
  - Upload de imágenes
  - Precios mayoristas
  - CORS configurado

### Frontend (Next.js)
- **Framework**: Next.js 15 con React 19
- **Estilos**: Tailwind CSS
- **Estado**: Redux Toolkit
- **Funcionalidades**:
  - Catálogo de productos
  - Formulario de pedidos
  - Carrito de compras
  - Vista de productos
  - Notificaciones con toast

## 🚀 Despliegue

### Frontend en Vercel

1. **Conectar repositorio**:
   ```bash
   # Subir código a GitHub
   git add .
   git commit -m "Proyecto listo para despliegue"
   git push origin main
   ```

2. **Configurar en Vercel**:
   - Ir a [vercel.com](https://vercel.com)
   - Importar proyecto desde GitHub
   - Configurar variables de entorno:
     - `NEXT_PUBLIC_API_URL`: URL del backend en Render

3. **Build settings**:
   - Framework: Next.js
   - Root Directory: `frontend`
   - Build Command: `npm run build`
   - Output Directory: `.next`

### Backend en Render

1. **Preparar repositorio**:
   - El backend debe estar en la carpeta `backend/`
   - Crear `requirements.txt`:
   ```
   fastapi==0.104.1
   uvicorn==0.24.0
   python-multipart==0.0.6
   pydantic==2.5.0
   ```

2. **Configurar en Render**:
   - Ir a [render.com](https://render.com)
   - Crear nuevo Web Service
   - Conectar repositorio GitHub
   - Configurar:
     - Environment: Python 3
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
     - Root Directory: `backend`

3. **Variables de entorno**:
   - PORT: (automático en Render)
   - Opcional: DATABASE_URL para PostgreSQL

## 📱 Funcionalidades

### Productos
- ✅ Listado de productos desde API
- ✅ Filtrado por categorías
- ✅ Imágenes con fallback
- ✅ Precios regulares y mayoristas
- ✅ Gestión de stock

### Pedidos
- ✅ Formulario de pedido integrado
- ✅ Validación de datos
- ✅ Notificaciones de éxito/error
- ✅ Envío a WhatsApp (pendiente integración)

### Administración
- ✅ API para crear productos
- ✅ Upload de imágenes
- ✅ Base de datos con productos de ejemplo

## 🛠️ Desarrollo Local

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Configuración
1. Copiar `.env.local.example` a `.env.local`
2. Configurar `NEXT_PUBLIC_API_URL=http://localhost:8000`

## 📋 Próximos Pasos

### Para el Cliente
1. **Subir imágenes de gorros**:
   - Usar endpoint `/upload-image`
   - Actualizar productos con nuevas URLs

2. **Personalizar contenido**:
   - Cambiar textos y colores
   - Agregar información de empresa
   - Configurar WhatsApp

3. **Configurar dominio**:
   - Comprar dominio personalizado
   - Configurar en Vercel

### Mejoras Futuras
- [ ] Integración con WhatsApp Business API
- [ ] Panel de administración
- [ ] Categorías dinámicas
- [ ] Sistema de usuarios
- [ ] Pasarela de pagos
- [ ] Analytics de ventas

## 🔧 Estructura de Archivos

```
nextjs-ecommerce-template-main/
├── backend/
│   ├── main.py              # API FastAPI
│   ├── uploads/             # Imágenes subidas
│   └── ecommerce.db         # Base de datos SQLite
├── frontend/
│   ├── src/
│   │   ├── components/      # Componentes React
│   │   ├── hooks/           # Custom hooks
│   │   ├── lib/             # API functions
│   │   ├── types/           # TypeScript types
│   │   └── app/             # App Router
│   ├── public/              # Assets estáticos
│   ├── .env.local           # Variables de entorno
│   └── package.json
└── README.md
```

## 📞 Soporte

Para dudas sobre el despliegue o funcionamiento:
- Verificar logs en Vercel/Render
- Comprobar variables de entorno
- Revisar conexión entre frontend y backend

---

**Estado**: ✅ Listo para despliegue
**Última actualización**: Diciembre 2024