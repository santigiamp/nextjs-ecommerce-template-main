import { Product, ProductCreate, PedidoRequest, PedidoResponse, ImageUploadResponse } from '@/types/product';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

// Función helper para manejar respuestas
async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({ detail: 'Error desconocido' }));
    throw new Error(errorData.detail || `Error ${response.status}: ${response.statusText}`);
  }
  return response.json();
}

// API de Productos
export const productAPI = {
  // Obtener todos los productos
  getProducts: async (categoria?: string, activo: boolean = true): Promise<Product[]> => {
    const params = new URLSearchParams();
    if (categoria) params.append('categoria', categoria);
    params.append('activo', activo.toString());
    
    const response = await fetch(`${API_URL}/productos?${params.toString()}`);
    const products = await handleResponse<Product[]>(response);
    
    return products;
  },

  // Obtener un producto específico
  getProduct: async (id: number): Promise<Product> => {
    const response = await fetch(`${API_URL}/productos/${id}`);
    return handleResponse<Product>(response);
  },

  // Crear nuevo producto
  createProduct: async (product: ProductCreate): Promise<Product> => {
    const response = await fetch(`${API_URL}/productos`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(product),
    });
    return handleResponse<Product>(response);
  },

  // Obtener categorías
  getCategories: async (): Promise<{ categorias: string[] }> => {
    const response = await fetch(`${API_URL}/categorias`);
    return handleResponse<{ categorias: string[] }>(response);
  },
};

// API de Pedidos
export const orderAPI = {
  // Crear pedido
  createOrder: async (pedido: PedidoRequest): Promise<PedidoResponse> => {
    const response = await fetch(`${API_URL}/pedidos`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(pedido),
    });
    return handleResponse<PedidoResponse>(response);
  },

  // Obtener pedidos (para uso interno)
  getOrders: async () => {
    const response = await fetch(`${API_URL}/pedidos`);
    return handleResponse(response);
  },
};

// API de Imágenes
export const imageAPI = {
  // Subir imagen
  uploadImage: async (file: File): Promise<ImageUploadResponse> => {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_URL}/upload-image`, {
      method: 'POST',
      body: formData,
    });
    return handleResponse<ImageUploadResponse>(response);
  },
};

// Hook personalizado para usar con React Query o SWR
export const apiEndpoints = {
  products: `${API_URL}/productos`,
  categories: `${API_URL}/categorias`,
  orders: `${API_URL}/pedidos`,
  uploadImage: `${API_URL}/upload-image`,
  health: `${API_URL}/health`,
};

// Función para verificar conexión con el backend
export const checkBackendConnection = async (): Promise<boolean> => {
  try {
    const response = await fetch(`${API_URL}/health`);
    return response.ok;
  } catch (error) {
    console.error('Error connecting to backend:', error);
    return false;
  }
};