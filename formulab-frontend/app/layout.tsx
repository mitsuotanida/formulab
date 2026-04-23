import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "FormuLab — Aprende a Formular Modelos de Optimización",
  description: "Plataforma gamificada para aprender formulación de modelos de programación matemática. CII 2750 UDP.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="es" className="dark">
      <body className="bg-background text-foreground font-sans antialiased min-h-screen">
        {children}
      </body>
    </html>
  );
}
