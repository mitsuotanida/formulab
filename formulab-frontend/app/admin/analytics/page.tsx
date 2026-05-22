"use client";
import { useEffect, useState } from "react";
import api from "@/lib/api";

const RA_LABELS: Record<number, string> = {
  1: "Definir variables", 2: "Función objetivo", 3: "Restricciones", 4: "Clasificar modelo", 5: "Estructuras especiales",
};

interface StudentRA { user_id: string; name: string; ra_1: number; ra_2: number; ra_3: number; ra_4: number; ra_5: number; }

export default function AdminAnalyticsPage() {
  const [data, setData] = useState<StudentRA[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/ra-tracking/class-summary").then((r) => setData(r.data)).finally(() => setLoading(false));
  }, []);

  function getCellColor(rate: number) {
    if (rate >= 80) return "bg-accent/30 text-accent";
    if (rate >= 60) return "bg-accent/15 text-accent/80";
    if (rate >= 40) return "bg-accent-warn/30 text-accent-warn";
    if (rate > 0) return "bg-destructive/20 text-destructive";
    return "bg-surface-2 text-foreground-muted";
  }

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold">📊 Analítica de Resultados de Aprendizaje</h1>
        <p className="text-foreground-muted text-sm mt-1">Tasa de logro (%) por estudiante y RA. Verde ≥80%, Amarillo ≥40%, Rojo &lt;40%</p>
      </div>

      <div className="card p-0 overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border">
              <th className="text-left px-6 py-4 text-foreground-muted font-medium text-xs uppercase tracking-wider sticky left-0 bg-surface">Estudiante</th>
              {[1, 2, 3, 4, 5].map((ra) => (
                <th key={ra} className="px-4 py-4 text-center text-xs text-foreground-muted font-medium uppercase tracking-wider min-w-32">
                  <div>RA{ra}</div>
                  <div className="font-normal text-foreground-muted/70 normal-case">{RA_LABELS[ra]}</div>
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {loading ? [...Array(5)].map((_, i) => (
              <tr key={i} className="border-b border-border">
                <td className="px-6 py-4"><div className="h-4 w-32 bg-surface-2 rounded animate-pulse" /></td>
                {[...Array(5)].map((_, j) => <td key={j} className="px-4 py-4"><div className="h-8 w-16 bg-surface-2 rounded animate-pulse mx-auto" /></td>)}
              </tr>
            )) : data.length === 0 ? (
              <tr><td colSpan={6} className="px-6 py-8 text-center text-foreground-muted">No hay datos de estudiantes aún.</td></tr>
            ) : data.map((student) => (
              <tr key={student.user_id} className="border-b border-border last:border-0 hover:bg-surface-2 transition-colors">
                <td className="px-6 py-4 font-medium sticky left-0 bg-surface">{student.name}</td>
                {[1, 2, 3, 4, 5].map((ra) => {
                  const rate = student[`ra_${ra}` as keyof StudentRA] as number;
                  return (
                    <td key={ra} className="px-4 py-4">
                      <div className={`mx-auto w-16 h-8 rounded-lg flex items-center justify-center text-xs font-bold ${getCellColor(rate)}`}>
                        {rate > 0 ? `${rate}%` : "—"}
                      </div>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="flex flex-wrap gap-3 text-xs">
        {[["bg-accent/30 text-accent", "≥80% — Logrado"], ["bg-accent-warn/30 text-accent-warn", "40-79% — En progreso"], ["bg-destructive/20 text-destructive", "<40% — Por desarrollar"], ["bg-surface-2 text-foreground-muted", "Sin intentos"]].map(([cls, label]) => (
          <div key={label} className="flex items-center gap-2">
            <div className={`w-8 h-5 rounded ${cls.split(" ")[0]}`} />
            <span className="text-foreground-muted">{label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
