"use client";

import Breadcrumb from "@/components/Common/Breadcrumb";
import React from "react";

const Signin = () => {
  const handleGoogleSignIn = () => {
    // Aquí se implementaría la lógica de autenticación con Google
    console.log('Iniciando sesión con Google...');
    // Por ahora, redirigir al catálogo como demo
    window.location.href = '/shop-with-sidebar';
  };

  const handleEmailSignIn = (e: React.FormEvent) => {
    e.preventDefault();
    // Aquí se implementaría la lógica de autenticación con email
    console.log('Iniciando sesión con email...');
    // Por ahora, redirigir al catálogo como demo
    window.location.href = '/shop-with-sidebar';
  };

  return (
    <>
      <Breadcrumb title={"Iniciar Sesión"} pages={["Iniciar Sesión"]} />
      <section 
        className="overflow-hidden py-20"
        style={{
          background: 'linear-gradient(135deg, #fed7aa 0%, #fef3c7 50%, #bbf7d0 100%)'
        }}
      >
        <div className="max-w-[1170px] w-full mx-auto px-4 sm:px-8 xl:px-0">
          <div className="max-w-[570px] w-full mx-auto rounded-xl bg-white shadow-lg p-4 sm:p-7.5 xl:p-11 border-l-4 border-orange-500">
            <div className="text-center mb-11">
              <h2 className="font-semibold text-xl sm:text-2xl xl:text-heading-5 text-gray-800 mb-1.5">
                Acceso para Mayoristas
              </h2>
              <p className="text-gray-600">Inicia sesión para acceder a precios mayoristas</p>
            </div>

            <div>
              {/* Información para mayoristas */}
              <div className="mb-8 p-4 rounded-lg bg-gradient-to-r from-blue-50 to-green-50 border border-blue-200">
                <h3 className="font-semibold text-gray-800 mb-2">🏪 Acceso Mayorista</h3>
                <p className="text-sm text-gray-600">
                  Al iniciar sesión tendrás acceso a:
                </p>
                <ul className="text-sm text-gray-600 mt-2 space-y-1">
                  <li>💰 Precios mayoristas especiales</li>
                  <li>📦 Pedidos mínimos por cantidad</li>
                  <li>🚚 Información de envíos</li>
                </ul>
              </div>

              {/* Botón de Google - Recomendado */}
              <div className="mb-6">
                <div className="text-center mb-3">
                  <span className="inline-block bg-gradient-to-r from-orange-400 to-yellow-400 text-white text-xs font-bold px-3 py-1 rounded-full">
                    ⚡ RECOMENDADO
                  </span>
                </div>
                <button 
                  onClick={handleGoogleSignIn}
                  className="w-full flex justify-center items-center gap-4 rounded-lg p-4 font-medium text-gray-700 border-2 border-green-300 hover:shadow-lg transition-all duration-200"
                  style={{
                    background: 'linear-gradient(90deg, #ffffff 0%, #f0fdf4 100%)'
                  }}
                >
                  <svg
                    width="24"
                    height="24"
                    viewBox="0 0 20 20"
                    fill="none"
                    xmlns="http://www.w3.org/2000/svg"
                  >
                    <g clipPath="url(#clip0_98_7461)">
                      <mask
                        id="mask0_98_7461"
                        maskUnits="userSpaceOnUse"
                        x="0"
                        y="0"
                        width="20"
                        height="20"
                      >
                        <path d="M20 0H0V20H20V0Z" fill="white" />
                      </mask>
                      <g mask="url(#mask0_98_7461)">
                        <path
                          d="M19.999 10.2218C20.0111 9.53429 19.9387 8.84791 19.7834 8.17737H10.2031V11.8884H15.8267C15.7201 12.5391 15.4804 13.162 15.1219 13.7195C14.7634 14.2771 14.2935 14.7578 13.7405 15.1328L13.7209 15.2571L16.7502 17.5568L16.96 17.5774C18.8873 15.8329 19.999 13.2661 19.999 10.2218Z"
                          fill="#4285F4"
                        />
                        <path
                          d="M10.2036 20C12.9586 20 15.2715 19.1111 16.9609 17.5777L13.7409 15.1332C12.8793 15.7223 11.7229 16.1333 10.2036 16.1333C8.91317 16.126 7.65795 15.7206 6.61596 14.9746C5.57397 14.2287 4.79811 13.1802 4.39848 11.9777L4.2789 11.9877L1.12906 14.3766L1.08789 14.4888C1.93622 16.1457 3.23812 17.5386 4.84801 18.512C6.45791 19.4852 8.31194 20.0005 10.2036 20Z"
                          fill="#34A853"
                        />
                        <path
                          d="M4.39899 11.9776C4.1758 11.3411 4.06063 10.673 4.05807 9.9999C4.06218 9.3279 4.1731 8.66067 4.38684 8.02221L4.38115 7.88959L1.1927 5.46234L1.0884 5.51095C0.372762 6.90337 0 8.44075 0 9.99983C0 11.5589 0.372762 13.0962 1.0884 14.4887L4.39899 11.9776Z"
                          fill="#FBBC05"
                        />
                        <path
                          d="M10.2039 3.86663C11.6661 3.84438 13.0802 4.37803 14.1495 5.35558L17.0294 2.59997C15.1823 0.90185 12.7364 -0.0298855 10.2039 -3.67839e-05C8.31239 -0.000477835 6.45795 0.514733 4.84805 1.48799C3.23816 2.46123 1.93624 3.85417 1.08789 5.51101L4.38751 8.02225C4.79107 6.82005 5.5695 5.77231 6.61303 5.02675C7.65655 4.28119 8.91254 3.87541 10.2039 3.86663Z"
                          fill="#EB4335"
                        />
                      </g>
                    </g>
                    <defs>
                      <clipPath id="clip0_98_7461">
                        <rect width="20" height="20" fill="white" />
                      </clipPath>
                    </defs>
                  </svg>
                  Acceso Automático con Google
                </button>
              </div>

              {/* Separador */}
              <div className="relative my-8">
                <div className="absolute inset-0 flex items-center">
                  <div className="w-full border-t border-gray-300"></div>
                </div>
                <div className="relative flex justify-center text-sm">
                  <span className="px-2 bg-white text-gray-500">o usa otro email</span>
                </div>
              </div>

              {/* Formulario de email */}
              <form onSubmit={handleEmailSignIn}>
                <div className="mb-5">
                  <label htmlFor="email" className="block mb-2.5 font-medium text-gray-700">
                    Email
                  </label>
                  <input
                    type="email"
                    name="email"
                    id="email"
                    placeholder="tucorreo@ejemplo.com"
                    required
                    className="rounded-lg border border-gray-300 bg-gray-50 placeholder:text-gray-400 w-full py-3 px-5 outline-none duration-200 focus:border-orange-400 focus:shadow-lg focus:ring-2 focus:ring-orange-200"
                  />
                </div>

                <div className="mb-5">
                  <label htmlFor="password" className="block mb-2.5 font-medium text-gray-700">
                    Contraseña
                  </label>
                  <input
                    type="password"
                    name="password"
                    id="password"
                    placeholder="Tu contraseña"
                    autoComplete="on"
                    required
                    className="rounded-lg border border-gray-300 bg-gray-50 placeholder:text-gray-400 w-full py-3 px-5 outline-none duration-200 focus:border-orange-400 focus:shadow-lg focus:ring-2 focus:ring-orange-200"
                  />
                </div>

                <button
                  type="submit"
                  className="w-full flex justify-center font-medium text-white py-3 px-6 rounded-lg ease-out duration-200 hover:shadow-lg mt-7.5"
                  style={{
                    background: 'linear-gradient(90deg, #f97316 0%, #eab308 100%)'
                  }}
                >
                  Iniciar Sesión
                </button>

                <p className="text-center mt-6 text-sm text-gray-600">
                  ¿Primera vez? El registro es automático al iniciar sesión
                </p>
              </form>
              
              <div className="mt-6 p-3 rounded-lg bg-yellow-50 border border-yellow-200">
                <p className="text-xs text-gray-600">
                  💡 <strong>Nota:</strong> Esta es una versión de demostración. 
                  Ambos métodos te llevarán directamente al catálogo.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </>
  );
};

export default Signin;
