"use client";
import { useState, useEffect } from "react";
import "../css/euclid-circular-a-font.css";
import "../css/style.css";
import Header from "../../components/Header";
import Footer from "../../components/Footer";

import { ModalProvider } from "../context/QuickViewModalContext";
import { CartModalProvider } from "../context/CartSidebarModalContext";
import { ReduxProvider } from "@/redux/provider";
import QuickViewModal from "@/components/Common/QuickViewModal";
import CartSidebarModal from "@/components/Common/CartSidebarModal";
import { PreviewSliderProvider } from "../context/PreviewSliderContext";
import PreviewSliderModal from "@/components/Common/PreviewSlider";

import ScrollToTop from "@/components/Common/ScrollToTop";
import PreLoader from "@/components/Common/PreLoader";
import WhatsAppButton from "@/components/Common/WhatsAppButton";
import { Toaster } from "react-hot-toast";
import { VisualEditing } from "@sanity/visual-editing/react";

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    setTimeout(() => setLoading(false), 1000);
  }, []);

  return (
    <html lang="en" suppressHydrationWarning={true} data-oid="l4dei89">
      <body data-oid="mlkav2.">
        {loading ? (
          <PreLoader data-oid="p8vrad0" />
        ) : (
          <>
            <ReduxProvider data-oid="7a48uij">
              <CartModalProvider data-oid="ylmq.4q">
                <ModalProvider data-oid="cvrnv7h">
                  <PreviewSliderProvider data-oid="gnzi.d_">
                    <Header data-oid="ofqqzvs" />
                    {children}

                    <QuickViewModal data-oid="vsb-ub4" />
                    <CartSidebarModal data-oid="rpn_j-6" />
                    <PreviewSliderModal data-oid="s-gyx_k" />
                  </PreviewSliderProvider>
                </ModalProvider>
              </CartModalProvider>
            </ReduxProvider>
            <ScrollToTop data-oid="yofi6j1" />
            <WhatsAppButton data-oid="uk_8e7p" />
            <Footer data-oid="65b6ngm" />
            <Toaster
              position="top-right"
              toastOptions={{
                duration: 4000,
                style: {
                  background: "#363636",
                  color: "#fff",
                },
              }}
              data-oid="eko0y2p"
            />

            {process.env.NODE_ENV === "development" && (
              <VisualEditing data-oid="hxohc9l" />
            )}
          </>
        )}
      </body>
    </html>
  );
}
