import React from "react";
import Image from "next/image";

const Footer = () => {
  const year = new Date().getFullYear();

  return (
    <footer className="bg-gradient-to-r from-blue-50 via-orange-50 to-yellow-50 py-12 mt-20 border-t-4 border-gradient-to-r border-orange-400">
      <div className="max-w-[1170px] mx-auto px-4 sm:px-8 xl:px-0">
        <div className="flex flex-col md:flex-row justify-between items-center gap-6">
          {/* Logo y empresa */}
          <div className="flex items-center gap-3">
            <Image
              src="/images/logo/ChatGPT Image 30 jun 2025, 17_26_11.png"
              alt="Distribuidora Alegría Logo"
              width={60}
              height={60}
              className="rounded-lg shadow-md"
            />
            <div>
              <h3 className="text-lg font-bold text-gray-800">Distribuidora Alegría</h3>
              <p className="text-sm text-gray-600">Mayorista de Juguetes y Gorros</p>
            </div>
          </div>

          {/* Info de contacto */}
          <div className="text-center md:text-right bg-white p-4 rounded-lg shadow-md border-l-4 border-green-400">
            <p className="text-gray-600 text-sm">
              Para pedidos mayoristas contacta por WhatsApp
            </p>
            <p className="text-green-600 font-bold text-lg">+54 9 11 XXXX-XXXX</p>
          </div>
        </div>
        
        {/* Copyright */}
        <div className="border-t border-orange-200 mt-8 pt-6 text-center">
          <p className="text-gray-600 text-sm">
            © {year} <span className="text-orange-600 font-medium">Distribuidora Alegría</span>. Todos los derechos reservados.
          </p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;