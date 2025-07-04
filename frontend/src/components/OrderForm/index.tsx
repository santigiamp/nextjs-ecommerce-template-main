"use client";
import React, { useState } from "react";
import { PedidoRequest } from "@/types/product";
import { orderAPI } from "@/lib/api";
import emailjs from '@emailjs/browser';
import { EMAILJS_CONFIG, EmailParams } from '@/lib/emailjs';

interface OrderFormProps {
  product: {
    id: number;
    nombre: string;
    precio: number;
  };
  onClose: () => void;
  onSuccess: (message: string) => void;
}

const OrderForm: React.FC<OrderFormProps> = ({ product, onClose, onSuccess }) => {
  const [formData, setFormData] = useState<PedidoRequest>({
    nombre: "",
    email: "",
    telefono: "",
    producto_id: product.id,
    producto_nombre: product.nombre,
    cantidad: 1,
    comentarios: "",
  });
  
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      // Enviar email usando EmailJS
      const emailParams = {
        from_name: formData.nombre,
        from_email: formData.email,
        phone: formData.telefono,
        product: formData.producto_nombre,
        quantity: formData.cantidad.toString(),
        comments: formData.comentarios || 'Sin comentarios adicionales',
        order_date: new Date().toLocaleString('es-ES', {
          day: '2-digit',
          month: '2-digit', 
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit'
        })
      };

      await emailjs.send(
        EMAILJS_CONFIG.SERVICE_ID,
        EMAILJS_CONFIG.TEMPLATE_ID,
        emailParams,
        EMAILJS_CONFIG.PUBLIC_KEY
      );

      // También guardar en el backend (opcional, para registros)
      try {
        const orderData = {
          ...formData,
          email_destino: "santinogiampietro7@gmail.com"
        };
        await orderAPI.createOrder(orderData);
      } catch (backendError) {
        console.log('Backend storage failed, but email was sent successfully');
      }
      
      onSuccess("¡Pedido enviado correctamente! Recibirás una respuesta pronto.");
      onClose();
    } catch (err) {
      console.error('Error al enviar pedido:', err);
      setError('Error al enviar el pedido. Por favor, verifica tu conexión e inténtalo de nuevo.');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: name === 'cantidad' ? parseInt(value) || 1 : value
    }));
  };

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4" style={{ zIndex: 9999 }}>
      <div 
        className="rounded-lg shadow-xl max-w-md w-full max-h-[90vh] overflow-y-auto border-l-4"
        style={{
          background: 'linear-gradient(135deg, #ffffff 0%, #fef3c7 100%)',
          borderLeftColor: '#f97316'
        }}
      >
        <div className="p-6">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold text-gray-800">🛒 Realizar Pedido</h2>
            <button
              onClick={onClose}
              className="text-gray-400 hover:text-orange-600 transition-colors"
            >
              <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <div className="mb-4 p-4 rounded-lg border-2 border-green-200" style={{ background: 'linear-gradient(90deg, #f0fdf4 0%, #dcfce7 100%)' }}>
            <h3 className="font-medium text-green-800">📦 {product.nombre}</h3>
            <p className="text-sm text-green-700">💰 Precio: ${product.precio}</p>
          </div>

          {error && (
            <div className="mb-4 p-3 bg-red-100 border border-red-400 text-red-700 rounded">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label htmlFor="nombre" className="block text-sm font-medium text-gray-700 mb-1">
                Nombre completo *
              </label>
              <input
                type="text"
                id="nombre"
                name="nombre"
                value={formData.nombre}
                onChange={handleInputChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-orange-400"
                placeholder="Tu nombre completo"
              />
            </div>

            <div>
              <label htmlFor="email" className="block text-sm font-medium text-gray-700 mb-1">
                Email de contacto *
              </label>
              <input
                type="email"
                id="email"
                name="email"
                value={formData.email}
                onChange={handleInputChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-orange-400"
                placeholder="tucorreo@ejemplo.com"
              />
            </div>

            <div>
              <label htmlFor="telefono" className="block text-sm font-medium text-gray-700 mb-1">
                Teléfono *
              </label>
              <input
                type="tel"
                id="telefono"
                name="telefono"
                value={formData.telefono}
                onChange={handleInputChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-orange-400"
                placeholder="Tu número de teléfono"
              />
            </div>

            <div>
              <label htmlFor="cantidad" className="block text-sm font-medium text-gray-700 mb-1">
                Cantidad *
              </label>
              <select
                id="cantidad"
                name="cantidad"
                value={formData.cantidad}
                onChange={handleInputChange}
                required
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-orange-400"
              >
                {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(num => (
                  <option key={num} value={num}>{num}</option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="comentarios" className="block text-sm font-medium text-gray-700 mb-1">
                Comentarios adicionales
              </label>
              <textarea
                id="comentarios"
                name="comentarios"
                value={formData.comentarios}
                onChange={handleInputChange}
                rows={3}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-orange-400 focus:border-orange-400"
                placeholder="Talla, color, instrucciones especiales..."
              />
            </div>

            <div className="flex gap-3 pt-4">
              <button
                type="button"
                onClick={onClose}
                className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-gray-500"
              >
                Cancelar
              </button>
              <button
                type="submit"
                disabled={loading}
                className="flex-1 px-4 py-2 text-white rounded-md hover:shadow-lg focus:outline-none focus:ring-2 focus:ring-green-400 disabled:opacity-50 font-medium"
                style={{
                  background: loading ? '#9ca3af' : 'linear-gradient(90deg, #16a34a 0%, #22c55e 100%)'
                }}
              >
                {loading ? "📤 Enviando..." : "✅ Confirmar Pedido"}
              </button>
            </div>
          </form>

          <div className="mt-4 p-3 rounded-lg border border-blue-200" style={{ background: 'linear-gradient(90deg, #eff6ff 0%, #dbeafe 100%)' }}>
            <p className="text-sm text-blue-800">
              <strong>📱 Nota:</strong> Nos contactaremos contigo por WhatsApp para confirmar tu pedido y coordinar la entrega.
            </p>
            <p className="text-xs text-blue-600 mt-1">
              📧 Tu pedido se enviará a: <strong>santinogiampietro7@gmail.com</strong>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default OrderForm;