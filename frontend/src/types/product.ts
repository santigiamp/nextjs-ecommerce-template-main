export type Product = {
  id: number;
  nombre: string;
  precio: number;
  descripcion: string;
  imagen_url: string;
  categoria: string;
  stock?: number;
  precio_mayorista?: number;
  minimo_mayorista?: number;
  activo: boolean;
};

export type ProductCreate = {
  nombre: string;
  precio: number;
  descripcion: string;
  imagen_url: string;
  categoria: string;
  stock?: number;
  precio_mayorista?: number;
  minimo_mayorista?: number;
  activo: boolean;
};

export type PedidoRequest = {
  nombre: string;
  telefono: string;
  producto_id: number;
  producto_nombre: string;
  cantidad: number;
  comentarios?: string;
};

export type PedidoResponse = {
  id: number;
  mensaje: string;
};

export type ImageUploadResponse = {
  filename: string;
  url: string;
  message: string;
};
