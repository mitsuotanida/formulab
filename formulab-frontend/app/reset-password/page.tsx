"use client";
import { Suspense, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Link from "next/link";
import api from "@/lib/api";

function ResetPasswordContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const token = searchParams.get("token") || "";
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [loading, setLoading] = useState(false);
  const [success, setSuccess] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (password !== confirm) { setError("Las contraseñas no coinciden"); return; }
    if (password.length < 8) { setError("La contraseña debe tener al menos 8 caracteres"); return; }
    setLoading(true);
    setError("");
    try {
      await api.post("/auth/reset-password", { token, new_password: password });
      setSuccess(true);
      setTimeout(() => router.replace("/login"), 3000);
    } catch (err: unknown) {
      const detail = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      setError(detail || "El enlace expiró o ya fue usado. Solicita uno nuevo.");
    } finally {
      setLoading(false);
    }
  }

  if (!token) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background px-4">
        <div className="card text-center space-y-4 max-w-md w-full">
          <div className="text-5xl">❌</div>
          <h2 className="text-xl font-semibold text-destructive">Enlace inválido</h2>
          <p className="text-foreground-muted text-sm">No se encontró el token de recuperación.</p>
          <Link href="/forgot-password" className="btn-primary block">Solicitar nuevo enlace</Link>
        </div>
      </div>
    );
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
          {success ? (
            <div className="text-center space-y-4">
              <div className="text-5xl">✅</div>
              <h2 className="text-xl font-semibold text-accent">Contraseña restablecida</h2>
              <p className="text-foreground-muted text-sm">Redirigiendo al inicio de sesión...</p>
              <Link href="/login" className="btn-primary block">Ir al inicio de sesión</Link>
            </div>
          ) : (
            <>
              <h2 className="text-xl font-semibold mb-2">Nueva contraseña</h2>
              <p className="text-foreground-muted text-sm mb-6">Elige una contraseña segura para tu cuenta.</p>
              {error && (
                <div className="bg-destructive/10 border border-destructive/30 text-destructive text-sm rounded-lg p-3 mb-4">
                  {error}
                </div>
              )}
              <form onSubmit={handleSubmit} className="space-y-4">
                <div>
                  <label className="text-sm text-foreground-muted mb-1.5 block">Nueva contraseña</label>
                  <input
                    type="password" value={password} onChange={(e) => setPassword(e.target.value)}
                    placeholder="Mínimo 8 caracteres" required className="input"
                  />
                </div>
                <div>
                  <label className="text-sm text-foreground-muted mb-1.5 block">Confirmar contraseña</label>
                  <input
                    type="password" value={confirm} onChange={(e) => setConfirm(e.target.value)}
                    placeholder="••••••••" required className="input"
                  />
                </div>
                <button type="submit" disabled={loading} className="btn-primary w-full">
                  {loading ? "Guardando..." : "Restablecer contraseña"}
                </button>
              </form>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default function ResetPasswordPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-foreground-muted">Cargando...</div>
      </div>
    }>
      <ResetPasswordContent />
    </Suspense>
  );
}
