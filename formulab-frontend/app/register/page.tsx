"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import api from "@/lib/api";
import { storeSession } from "@/lib/auth";

export default function RegisterPage() {
  const router = useRouter();
  const [form, setForm] = useState({ name: "", email: "", password: "", confirm: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  function handleChange(e: React.ChangeEvent<HTMLInputElement>) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    if (form.password !== form.confirm) { setError("Las contraseñas no coinciden"); return; }
    setLoading(true); setError("");
    try {
      const { data } = await api.post("/auth/register", { name: form.name, email: form.email, password: form.password });
      storeSession(data.access_token, data.refresh_token, data.user);
      router.replace("/dashboard");
    } catch (err: unknown) {
      const msg = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail;
      setError(msg || "Error al registrar usuario");
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
          <h1 className="text-3xl font-bold">FormuLab</h1>
          <p className="text-foreground-muted mt-2">Crea tu cuenta de estudiante</p>
        </div>

        <div className="card">
          <h2 className="text-xl font-semibold mb-6">Registro</h2>
          {error && (
            <div className="bg-destructive/10 border border-destructive/30 text-destructive text-sm rounded-lg p-3 mb-4">
              {error}
            </div>
          )}
          <form onSubmit={handleSubmit} className="space-y-4">
            {[
              { label: "Nombre completo", name: "name", type: "text", placeholder: "Juan Pérez" },
              { label: "Email institucional", name: "email", type: "email", placeholder: "juan@mail.udp.cl" },
              { label: "Contraseña", name: "password", type: "password", placeholder: "••••••••" },
              { label: "Confirmar contraseña", name: "confirm", type: "password", placeholder: "••••••••" },
            ].map((f) => (
              <div key={f.name}>
                <label className="text-sm text-foreground-muted mb-1.5 block">{f.label}</label>
                <input
                  type={f.type} name={f.name} value={form[f.name as keyof typeof form]}
                  onChange={handleChange} placeholder={f.placeholder} required className="input"
                />
              </div>
            ))}
            <button type="submit" disabled={loading} className="btn-primary w-full mt-2">
              {loading ? "Creando cuenta..." : "Crear cuenta"}
            </button>
          </form>
          <p className="text-center text-foreground-muted text-sm mt-4">
            ¿Ya tienes cuenta?{" "}
            <Link href="/login" className="text-primary hover:text-primary-light transition-colors">
              Inicia sesión
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
