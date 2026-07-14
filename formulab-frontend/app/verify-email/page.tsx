"use client";
import { Suspense, useEffect, useState } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Link from "next/link";
import api from "@/lib/api";

type Status = "loading" | "success" | "error";

function VerifyEmailContent() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const token = searchParams.get("token");
  const [status, setStatus] = useState<Status>("loading");
  const [message, setMessage] = useState("");

  useEffect(() => {
    if (!token) {
      setStatus("error");
      setMessage("Enlace inválido. No se encontró el token de verificación.");
      return;
    }
    api.get(`/auth/verify-email?token=${encodeURIComponent(token)}`)
      .then(() => {
        setStatus("success");
        setMessage("Cuenta verificada exitosamente.");
        setTimeout(() => router.replace("/login"), 3000);
      })
      .catch((err) => {
        const detail = err?.response?.data?.detail;
        setStatus("error");
        setMessage(detail || "El enlace expiró o ya fue usado. Solicita uno nuevo desde el dashboard.");
      });
  }, [token]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-background px-4">
      <div className="w-full max-w-md">
        <div className="text-center mb-8">
          <div className="inline-flex items-center justify-center w-16 h-16 rounded-2xl bg-primary/20 border border-primary/30 mb-4">
            <span className="text-3xl">⚡</span>
          </div>
          <h1 className="text-3xl font-bold text-foreground">FormuLab</h1>
        </div>

        <div className="card text-center space-y-4">
          {status === "loading" && (
            <>
              <div className="text-4xl animate-pulse">📬</div>
              <p className="text-foreground-muted">Verificando tu cuenta...</p>
            </>
          )}

          {status === "success" && (
            <>
              <div className="text-5xl">✅</div>
              <h2 className="text-xl font-semibold text-accent">{message}</h2>
              <p className="text-foreground-muted text-sm">Redirigiendo al inicio de sesión...</p>
              <Link href="/login" className="btn-primary block">Ir al inicio de sesión</Link>
            </>
          )}

          {status === "error" && (
            <>
              <div className="text-5xl">❌</div>
              <h2 className="text-xl font-semibold text-destructive">Verificación fallida</h2>
              <p className="text-foreground-muted text-sm">{message}</p>
              <Link href="/login" className="btn-primary block">Volver al inicio de sesión</Link>
            </>
          )}
        </div>
      </div>
    </div>
  );
}

export default function VerifyEmailPage() {
  return (
    <Suspense fallback={
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-foreground-muted">Cargando...</div>
      </div>
    }>
      <VerifyEmailContent />
    </Suspense>
  );
}
