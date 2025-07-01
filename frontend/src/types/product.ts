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
  email: string;
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

export type Order = {
  id: number;
  nombre: string;
  email: string;
  telefono: string;
  producto_id: number;
  producto_nombre: string;
  cantidad: number;
  comentarios?: string;
  fecha_pedido?: string;
  estado: string;
};

export type OrderModalProps = {
  showDetails: boolean;
  showEdit: boolean;
  toggleModal: (state: boolean) => void;
  order: Order;
};

export type EditOrderProps = {
  order: Order;
  toggleModal: (state: boolean) => void;
};
