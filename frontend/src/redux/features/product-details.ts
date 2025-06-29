import { createSlice } from "@reduxjs/toolkit";
import { Product } from "@/types/product";

type InitialState = {
  value: Product;
};

const initialState = {
  value: {
    id: 0,
    nombre: "",
    precio: 0,
    descripcion: "",
    imagen_url: "",
    categoria: "",
    stock: 0,
    precio_mayorista: 0,
    minimo_mayorista: 0,
    activo: false,
  },
} as InitialState;

export const productDetails = createSlice({
  name: "productDetails",
  initialState,
  reducers: {
    updateproductDetails: (_, action) => {
      return {
        value: {
          ...action.payload,
        },
      };
    },
  },
});

export const { updateproductDetails } = productDetails.actions;
export default productDetails.reducer;
