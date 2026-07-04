"use client";
import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import api from "@/lib/api";
import { getStoredUser } from "@/lib/auth";
import { LEVEL_NAMES, DIFFICULTY_LABELS, TYPE_LABELS, type Exercise } from "@/lib/types";

interface Analytics { total_students: number; total_submissions: number; avg_score: number; total_exercises: number; }

function XPBar({ xp, level }: { xp: number; level: number }) {
  const thresholds = [0, 500, 1500, 3500, 7500, 15000, Infinity];
  const min = thresholds[level - 1] || 0;
  const max = thresholds[level] || 15000;
  const pct = Math.min(100, Math.round(((xp - min) / (max - min)) * 100));
  return (
    <div>
      <div className="flex justify-between text-xs text-foreground-muted mb-1.5">
        <span>{LEVEL_NAMES[level]}</span>
        <span>{xp.toLocaleString()} / {max === Infinity ? "∞" : max.toLocaleString()} XP</span>
      </div>
      <div className="h-2 bg-surface-2 rounded-full overflow-hidden">
        <div className="h-full bg-gradient-to-r from-primary to-primary-light rounded-full transition-all duration-500" style={{ width: `${pct}%` }} />
      </div>
    </div>
  );
}

export default function DashboardPage() {
  const user = getStoredUser();
  const router = useRouter();
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [analytics, setAnalytics] = useState<Analytics | null>(null);
  const [loading, setLoading] = useState(true);
  const [resending, setResending] = useState(false);
  const [resentOk, setResentOk] = useState(false);

  async function resendVerification() {
    if (!user) return;
    setResending(true);
    try {
      await api.post("/auth/resend-verification", { email: user.email });
      setResentOk(true);
    } finally {
      setResending(false);
    }
  }

  useEffect(() => {
    if (!user) { router.replace("/login"); return; }
    Promise.all([
      api.get("/exercises?page=1&per_page=4"),
      user.role === "teacher" ? api.get("/admin/analytics").catch(() => ({ data: null })) : Promise.resolve({ data: null }),
    ]).then(([exRes, anRes]) => {
      setExercises(exRes.data.data || []);
      setAnalytics(anRes.data);
    }).finally(() => setLoading(false));
  }, []);

  if (!user) return null;

  return (
    <div className="space-y-8 animate-fade-in">
      {!user.is_verified && (
        <div className="bg-accent-warn/10 border border-accent-warn/40 rounded-xl px-4 py-3 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3">
          <div>
            <p className="text-accent-warn font-medium text-sm">⚠️ Verifica tu cuenta</p>
            <p className="text-foreground-muted text-xs mt-0.5">
              Revisa tu email y haz clic en el enlace de verificación para activar todas las funciones.
            </p>
          </div>
          {resentOk ? (
            <span className="text-accent text-sm shrink-0">✅ Enlace reenviado</span>
          ) : (
            <button onClick={resendVerification} disabled={resending} className="btn-secondary text-sm shrink-0 whitespace-nowrap">
              {resending ? "Enviando..." : "Reenviar enlace"}
            </button>
          )}
        </div>
      )}

      <div>
        <h1 className="text-2xl font-bold">Hola, {user.nickname || user.name.split(" ")[0]} 👋</h1>
        <p className="text-foreground-muted mt-1">Bienvenido a FormuLab — CII 2750 Optimización</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="card col-span-2">
          <div className="flex items-center justify-between mb-4">
            <div>
              <p className="text-foreground-muted text-sm">Nivel actual</p>
              <p className="text-2xl font-bold text-primary">{LEVEL_NAMES[user.level]}</p>
            </div>
            <div className="text-right">
              <p className="text-foreground-muted text-sm">Racha</p>
              <p className="text-2xl font-bold text-accent-warn">🔥 {user.streak} días</p>
            </div>
          </div>
          <XPBar xp={user.xp} level={user.level} />
        </div>
        <div className="card flex flex-col items-center justify-center text-center">
          <p className="text-4xl font-bold font-mono text-accent">{user.xp.toLocaleString()}</p>
          <p className="text-foreground-muted text-sm mt-1">XP Total</p>
        </div>
      </div>

      {user.role === "teacher" && analytics && (
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          {[
            { label: "Estudiantes", value: analytics.total_students, icon: "👥" },
            { label: "Submissions", value: analytics.total_submissions, icon: "📝" },
            { label: "Puntaje Prom.", value: `${analytics.avg_score}%`, icon: "📊" },
            { label: "Ejercicios", value: analytics.total_exercises, icon: "📐" },
          ].map((stat) => (
            <div key={stat.label} className="card flex items-center gap-4">
              <span className="text-2xl">{stat.icon}</span>
              <div>
                <p className="text-xl font-bold">{stat.value}</p>
                <p className="text-foreground-muted text-xs">{stat.label}</p>
              </div>
            </div>
          ))}
        </div>
      )}

      <div>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-semibold">Ejercicios Recientes</h2>
          <Link href="/exercises" className="text-primary text-sm hover:text-primary-light transition-colors">Ver todos →</Link>
        </div>
        {loading ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {[...Array(4)].map((_, i) => <div key={i} className="card h-32 animate-pulse bg-surface-2" />)}
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {exercises.map((ex) => (
              <Link key={ex.id} href={`/exercises/${ex.id}`} className="card-hover block">
                <div className="flex items-start justify-between gap-2 mb-3">
                  <h3 className="font-medium text-sm line-clamp-2">{ex.title}</h3>
                  {ex.user_best_score !== null && ex.user_best_score !== undefined && (
                    <span className={`text-xs font-bold shrink-0 ${ex.user_best_score >= 70 ? "text-accent" : "text-accent-warn"}`}>
                      {ex.user_best_score}%
                    </span>
                  )}
                </div>
                <div className="flex gap-2 flex-wrap">
                  <span className="badge-type">{TYPE_LABELS[ex.type]}</span>
                  <span className={`badge-difficulty-${ex.difficulty}`}>{DIFFICULTY_LABELS[ex.difficulty]}</span>
                </div>
              </Link>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
