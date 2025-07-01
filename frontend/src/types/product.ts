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

// Legacy order item interface for existing orders data
export interface OrderItem {
  orderId: string;
  createdAt: string;
  status: 'delivered' | 'processing' | 'on-hold' | 'cancelled';
  total: string;
  title: string;
}

// Props for OrderActions component
export interface OrderActionsProps {
  toggleEdit: () => void;
  toggleDetails: () => void;
}

// Props for OrderDetails component  
export interface OrderDetailsProps {
  orderItem: OrderItem;
}

// Props for SingleOrder component
export interface SingleOrderProps {
  orderItem: OrderItem;
  smallView?: boolean;
}

// Props for Breadcrumb component
export interface BreadcrumbProps {
  title: string;
  pages: string[];
}

// Cart item interface
export interface CartItem {
  id: number;
  title: string;
  price: number;
  discountedPrice: number;
  quantity: number;
  imgs?: {
    thumbnails: string[];
    previews?: string[];
  };
}

// Wishlist item interface (similar to CartItem but with different properties)  
export interface WishlistItem {
  id: number;
  title: string;
  price: number;
  discountedPrice: number;
  imgs?: {
    thumbnails: string[];
    previews: string[];
  };
}

// Product interface for shop/catalog display
export interface ProductDisplayItem {
  id: number;
  title: string;
  price: number;
  discountedPrice?: number;
  imgs?: {
    thumbnails: string[];
  };
}

// Category interface for blog/product categories
export interface CategoryItem {
  id: number;
  title: string;
  count?: number;
}

// Props for Blog components
export interface BlogCategoriesProps {
  categories: CategoryItem[];
}

export interface LatestPostsProps {
  blogs: import('./blogItem').BlogItem[];
}

export interface LatestProductsProps {
  products: ProductDisplayItem[];
}

// Props for Cart and Wishlist SingleItem components
export interface CartSingleItemProps {
  item: CartItem;
}

export interface WishlistSingleItemProps {
  item: WishlistItem;
}

// Props for Header Dropdown component
export interface HeaderDropdownProps {
  menuItem: {
    title: string;
    submenu: Array<{
      title: string;
      path: string;
    }>;
  };
  stickyMenu: boolean;
}

// Option interface for select dropdowns
export interface SelectOption {
  label: string;
  value: string | number;
}

// Category item for filters
export interface FilterCategoryItem {
  name: string;
  products: number;
}

// Gender item for filters  
export interface FilterGenderItem {
  name: string;
  products: number;
}

// Props for ShopWithSidebar components
export interface CustomSelectProps {
  options: SelectOption[];
}

export interface CategoryDropdownProps {
  categories: FilterCategoryItem[];
}

export interface GenderDropdownProps {
  genders: FilterGenderItem[];
}

export interface CategoryItemProps {
  category: FilterCategoryItem;
}

export interface GenderItemProps {
  category: FilterGenderItem;
}

// Props for CartSidebarModal SingleItem component
export interface CartSidebarSingleItemProps {
  item: CartItem;
  removeItemFromCart: (id: number) => any; // Redux action
}

// Props for AddressModal component
export interface AddressModalProps {
  isOpen: boolean;
  closeModal: () => void;
}
