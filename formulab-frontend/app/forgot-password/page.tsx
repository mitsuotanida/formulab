"use client";
import { useState } from "react";
import Link from "next/link";
import api from "@/lib/api";

export default function ForgotPasswordPage() {
  const [email, setEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const [sent, setSent] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await api.post("/auth/forgot-password", { email });
      setSent(true);
    } catch {
      setError("Ocurrió un error. Inténtalo de nuevo.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-background px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-primary/20 border border-primary/30 mb-4">
            <span className="text-3xl">⚡</span>
          </div>
          <h1 className="text-3xl font-bold text-foreground">FormuLab</h1>
        </div>

        <div className="card">
          {sent ? (
            <div className="text-center space-y-4">
              <div className="text-5xl">📬</div>
              <h2 className="text-xl font-semibold">Revisa tu correo</h2>
              <p className="text-foreground-muted text-sm">
                Si el email <span className="text-foreground font-medium">{email}</span> está registrado,
                recibirás un enlace para restablecer tu contraseña. El enlace expira en 15 minutos.
              </p>
              <p className="text-foreground-muted text-xs">Si no ves el correo, revisa tu carpeta de spam.</p>
              <Link href="/login" className="btn-primary block text-center">Volver al inicio de sesión</Link>
            </div>
          ) : (
            <>
              <h2 className="text-xl font-semibold mb-2">Olvidé mi contraseña</h2>
              <p className="text-foreground-muted text-sm mb-6">
                Ingresa tu email y te enviaremos un enlace para restablecer tu contraseña.
              </p>
              {error && (
                <div className="bg-destructive/10 border border-destructive/30 text-destructive text-sm rounded-lg p-3 mb-4">
                  {error}
                </div>
              )}
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="text-sm text-foreground-muted mb-1.5 block">Email institucional</label>
                  <input
                    type="email" value={email} onChange={(e) => setEmail(e.target.value)}
                    placeholder="usuario@mail.udp.cl" required className="input"
                  />
                </div>
                <button type="submit" disabled={loading} className="btn-primary w-full">
                  {loading ? "Enviando..." : "Enviar enlace de recuperación"}
                </button>
              </form>
              <p className="text-center text-foreground-muted text-sm mt-4">
                <Link href="/login" className="text-primary hover:text-primary-light transition-colors">
                  Volver al inicio de sesión
                </Link>
              </p>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
