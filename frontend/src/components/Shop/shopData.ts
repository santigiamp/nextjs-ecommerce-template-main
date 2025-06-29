import { Product } from "@/types/product";
import { productAPI } from "@/lib/api";

// Función para obtener productos desde la API
export const getShopData = async (categoria?: string): Promise<Product[]> => {
  try {
    return await productAPI.getProducts(categoria);
  } catch (error) {
    console.error('Error fetching products:', error);
    return [];
  }
};

// Función para obtener un producto específico
export const getProductById = async (id: number): Promise<Product | null> => {
  try {
    return await productAPI.getProduct(id);
  } catch (error) {
    console.error('Error fetching product:', error);
    return null;
  }
};

// Función para obtener categorías
export const getCategories = async (): Promise<string[]> => {
  try {
    const response = await productAPI.getCategories();
    return response.categorias;
  } catch (error) {
    console.error('Error fetching categories:', error);
    return [];
  }
};

// Datos de respaldo para desarrollo (en caso de que el backend no esté disponible)
const fallbackData: Product[] = [
  {
    id: 1,
    nombre: "Gorro de Invierno Unicornio",
    precio: 2500.00,
    descripcion: "Gorro térmico para niñas con diseño de unicornio. Tallas 2-8 años. Material: acrílico suave.",
    imagen_url: "https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=400&fit=crop",
    categoria: "Gorros",
    stock: 50,
    precio_mayorista: 2000.00,
    minimo_mayorista: 5,
    activo: true
  },
  {
    id: 2,
    nombre: "Gorro Polar Dinosaurio",
    precio: 2200.00,
    descripcion: "Gorro polar con orejas de dinosaurio. Perfecto para niños aventureros. Tallas 3-10 años.",
    imagen_url: "https://images.unsplash.com/photo-1607083206869-4c7672e72a8a?w=400&h=400&fit=crop",
    categoria: "Gorros",
    stock: 30,
    precio_mayorista: 1800.00,
    minimo_mayorista: 5,
    activo: true
  }
];

export default fallbackData;
