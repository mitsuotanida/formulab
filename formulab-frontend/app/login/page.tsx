"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import api from "@/lib/api";
import { storeSession } from "@/lib/auth";

export default function LoginPage() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const { data } = await api.post("/auth/login", { email, password });
      storeSession(data.access_token, data.refresh_token, data.user);
      router.replace("/dashboard");
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      setError(msg || "Credenciales inválidas");
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
          <p className="text-foreground-muted mt-2">Plataforma de Formulación Matemática</p>
        </div>

        <div className="card">
          <h2 className="text-xl font-semibold mb-6">Iniciar Sesión</h2>
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
                placeholder="estudiante@mail.udp.cl" required className="input"
              />
            </div>
            <div>
              <label className="text-sm text-foreground-muted mb-1.5 block">Contraseña</label>
              <input
                type="password" value={password} onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••" required className="input"
              />
            </div>
            <button type="submit" disabled={loading} className="btn-primary w-full mt-2">
              {loading ? "Iniciando sesión..." : "Ingresar"}
            </button>
          </form>
          <p className="text-center text-foreground-muted text-sm mt-4">
            ¿No tienes cuenta?{" "}
            <Link href="/register" className="text-primary hover:text-primary-light transition-colors">
              Regístrate aquí
            </Link>
          </p>
        </div>

        <p className="text-center text-foreground-muted text-xs mt-6">
          CII 2750 Optimización · Universidad Diego Portales
        </p>
      </div>
    </div>
  );
}
