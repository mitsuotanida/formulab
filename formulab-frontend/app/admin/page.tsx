"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import api from "@/lib/api";

interface Analytics {
  total_students: number;
  total_submissions: number;
  avg_score: number;
  total_exercises: number;
  ai_exercises: number;
  exercises_by_type: Record<string, number>;
  exercises_by_difficulty: Record<string, number>;
}

export default function AdminPage() {
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/admin/analytics").then((r) => setAnalytics(r.data)).finally(() => setLoading(false));
  }, []);

  function handleExport(endpoint: string, filename: string) {
    api.get(endpoint, { responseType: "blob" }).then((r) => {
      const url = URL.createObjectURL(new Blob([r.data]));
      const a = document.createElement("a");
      a.href = url; a.download = filename; a.click();
      URL.revokeObjectURL(url);
    });
  }

  return (
    <div className="space-y-8 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">🛠️ Panel de Administración</h1>
          <p className="text-foreground-muted text-sm mt-1">Gestión del curso CII 2750 Optimización</p>
        </div>
        <div className="flex gap-3">
          <button onClick={() => handleExport("/admin/export/students", "formulab_estudiantes.csv")} className="btn-secondary text-sm">
            📥 Exportar estudiantes
          </button>
          <button onClick={() => handleExport("/admin/export/ra-report", "formulab_ra_report.csv")} className="btn-secondary text-sm">
            📊 Exportar RAs
          </button>
        </div>
      </div>

      {loading ? (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[...Array(4)].map((_, i) => <div key={i} className="card h-24 animate-pulse bg-surface-2" />)}
        </div>
      ) : analytics && (
        <>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: "Estudiantes", value: analytics.total_students, icon: "👥", color: "text-primary" },
              { label: "Submissions", value: analytics.total_submissions, icon: "📝", color: "text-accent" },
              { label: "Puntaje promedio", value: `${analytics.avg_score}%`, icon: "📊", color: "text-accent-warn" },
              { label: "Ejercicios activos", value: analytics.total_exercises, icon: "📐", color: "text-primary-light" },
            ].map((s) => (
              <div key={s.label} className="card">
                <div className="flex items-center gap-3">
                  <span className="text-2xl">{s.icon}</span>
                  <div>
                    <p className={`text-2xl font-bold ${s.color}`}>{s.value}</p>
                    <p className="text-foreground-muted text-xs">{s.label}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="card">
              <h3 className="font-semibold mb-4">Ejercicios por tipo</h3>
              {Object.entries(analytics.exercises_by_type).map(([type, count]) => (
                <div key={type} className="flex items-center gap-3 mb-3">
                  <span className="badge-type w-16 text-center">{type}</span>
                  <div className="flex-1 h-2 bg-surface-2 rounded-full overflow-hidden">
                    <div className="h-full bg-primary rounded-full" style={{ width: `${(count / analytics.total_exercises) * 100}%` }} />
                  </div>
                  <span className="text-sm text-foreground-muted w-6">{count}</span>
                </div>
              ))}
            </div>
            <div className="card">
              <h3 className="font-semibold mb-4">Ejercicios por dificultad</h3>
              {[["easy", "Fácil", "text-accent"], ["medium", "Medio", "text-accent-warn"], ["hard", "Difícil", "text-destructive"]].map(([key, label, color]) => {
                const count = analytics.exercises_by_difficulty[key] || 0;
                return (
                  <div key={key} className="flex items-center gap-3 mb-3">
                    <span className={`text-sm w-16 ${color}`}>{label}</span>
                    <div className="flex-1 h-2 bg-surface-2 rounded-full overflow-hidden">
                      <div className={`h-full rounded-full ${color === "text-accent" ? "bg-accent" : color === "text-accent-warn" ? "bg-accent-warn" : "bg-destructive"}`} style={{ width: `${(count / analytics.total_exercises) * 100}%` }} />
                    </div>
                    <span className="text-sm text-foreground-muted w-6">{count}</span>
                  </div>
                );
              })}
            </div>
          </div>
        </>
      )}

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {[
          { href: "/admin/students", title: "Ver Estudiantes", desc: "Progreso individual, RA por alumno", icon: "👥" },
          { href: "/admin/exercises", title: "Gestionar Ejercicios", desc: "Crear, editar y generar con IA", icon: "📋" },
          { href: "/admin/analytics", title: "Analítica Completa", desc: "Heatmap de RAs por estudiante", icon: "📊" },
        ].map((item) => (
          <Link key={item.href} href={item.href} className="card-hover">
            <span className="text-3xl">{item.icon}</span>
            <h3 className="font-semibold mt-3">{item.title}</h3>
            <p className="text-foreground-muted text-sm mt-1">{item.desc}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}
