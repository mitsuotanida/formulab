"use client";
import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import api from "@/lib/api";
import { LEVEL_NAMES, type RATracking } from "@/lib/types";
import { RadarChart, PolarGrid, PolarAngleAxis, Radar, ResponsiveContainer } from "recharts";

interface StudentDetail { id: string; name: string; email: string; xp: number; level: number; streak: number; }

export default function StudentDetailPage() {
  const { id } = useParams<{ id: string }>();
  const [student, setStudent] = useState<StudentDetail | null>(null);
  const [ra, setRa] = useState<RATracking[]>([]);

  useEffect(() => {
    Promise.all([api.get(`/users/${id}`), api.get(`/ra-tracking/${id}`)]).then(([s, r]) => {
      setStudent(s.data);
      setRa(r.data.data);
    });
  }, [id]);

  if (!student) return <div className="animate-pulse text-foreground-muted">Cargando...</div>;

  const chartData = ra.map((r) => ({ ra: `RA${r.ra_id}`, value: Math.round(r.success_rate * 100) }));

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="card flex items-center gap-6">
        <div className="w-16 h-16 rounded-xl bg-primary/20 flex items-center justify-center text-3xl font-bold text-primary">
          {student.name[0]}
        </div>
        <div>
          <h1 className="text-xl font-bold">{student.name}</h1>
          <p className="text-foreground-muted">{student.email}</p>
          <div className="flex gap-4 mt-1">
            <span className="text-primary text-sm">{LEVEL_NAMES[student.level]}</span>
            <span className="text-accent font-mono text-sm">{student.xp.toLocaleString()} XP</span>
            <span className="text-accent-warn text-sm">🔥 {student.streak} días</span>
          </div>
        </div>
      </div>

      <div className="card">
        <h2 className="font-semibold mb-4">Resultados de Aprendizaje</h2>
        <ResponsiveContainer width="100%" height={220}>
          <RadarChart data={chartData}>
            <PolarGrid stroke="#2A2A3D" />
            <PolarAngleAxis dataKey="ra" tick={{ fill: "#9CA3AF", fontSize: 12 }} />
            <Radar dataKey="value" stroke="#6366F1" fill="#6366F1" fillOpacity={0.2} />
          </RadarChart>
        </ResponsiveContainer>
        <div className="grid grid-cols-1 md:grid-cols-5 gap-3 mt-4">
          {ra.map((r) => (
            <div key={r.ra_id} className="text-center">
              <p className="text-xs text-foreground-muted mb-1">RA{r.ra_id}</p>
              <p className={`text-lg font-bold ${r.success_rate >= 0.7 ? "text-accent" : r.success_rate >= 0.4 ? "text-accent-warn" : "text-destructive"}`}>
                {Math.round(r.success_rate * 100)}%
              </p>
              <p className="text-xs text-foreground-muted">{r.successes}/{r.attempts}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
