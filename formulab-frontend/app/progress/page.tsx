"use client";
import { useEffect, useState } from "react";
import api from "@/lib/api";
import { getStoredUser } from "@/lib/auth";
import { LEVEL_NAMES } from "@/lib/types";

interface ProgressStats {
  user_xp: number;
  user_percentile: number;
  count: number;
  min: number;
  q1: number;
  median: number;
  q3: number;
  max: number;
  mean: number;
}

const LEVELS_DATA = [
  { level: 1, name: "Pasante",     minXp: 0,     maxXp: 500,   icon: "🌱" },
  { level: 2, name: "Analista",    minXp: 500,   maxXp: 1500,  icon: "📐" },
  { level: 3, name: "Formulador",  minXp: 1500,  maxXp: 3500,  icon: "⚙️" },
  { level: 4, name: "Optimizador", minXp: 3500,  maxXp: 7500,  icon: "📊" },
  { level: 5, name: "Especialista",minXp: 7500,  maxXp: 15000, icon: "🎯" },
  { level: 6, name: "Maestro",     minXp: 15000, maxXp: null,  icon: "🏆" },
];

function BoxPlot({ stats }: { stats: ProgressStats }) {
  const PAD_L = 32, PAD_R = 32;
  const W = 560, H = 110;
  const INNER = W - PAD_L - PAD_R;
  const maxRange = Math.max(stats.max, stats.user_xp, 100);
  const sx = (v: number) => PAD_L + Math.min(v / maxRange, 1) * INNER;
  const MID_Y = 54, BOX_H = 34, HALF = BOX_H / 2;

  const userX = sx(stats.user_xp);
  const medX = sx(stats.median);
  const meanX = sx(stats.mean);

  const userLabelSide = userX > W * 0.75 ? "end" : "middle";

  return (
    <svg viewBox={`0 0 ${W} ${H}`} className="w-full" aria-label="Diagrama de caja del grupo">
      {/* Background track */}
      <rect x={PAD_L} y={MID_Y - 1} width={INNER} height={2} fill="currentColor" fillOpacity="0.06" rx="1" />

      {/* Whisker */}
      <line x1={sx(stats.min)} y1={MID_Y} x2={sx(stats.max)} y2={MID_Y}
        stroke="#6366F1" strokeWidth="1.5" strokeOpacity="0.5" />
      <line x1={sx(stats.min)} y1={MID_Y - 12} x2={sx(stats.min)} y2={MID_Y + 12}
        stroke="#6366F1" strokeWidth="2" />
      <line x1={sx(stats.max)} y1={MID_Y - 12} x2={sx(stats.max)} y2={MID_Y + 12}
        stroke="#6366F1" strokeWidth="2" />

      {/* IQR Box */}
      <rect
        x={sx(stats.q1)} y={MID_Y - HALF}
        width={Math.max(sx(stats.q3) - sx(stats.q1), 4)} height={BOX_H}
        fill="#6366F115" stroke="#6366F1" strokeWidth="2" rx="6"
      />

      {/* Mean (dashed) */}
      <line x1={meanX} y1={MID_Y - HALF + 8} x2={meanX} y2={MID_Y + HALF - 8}
        stroke="#9CA3AF" strokeWidth="1.5" strokeDasharray="4 3" />

      {/* Median */}
      <line x1={medX} y1={MID_Y - HALF} x2={medX} y2={MID_Y + HALF}
        stroke="#10B981" strokeWidth="3" strokeLinecap="round" />

      {/* User glow + dot */}
      <circle cx={userX} cy={MID_Y} r="13" fill="#F59E0B" fillOpacity="0.18" />
      <circle cx={userX} cy={MID_Y} r="7"  fill="#F59E0B" />
      <circle cx={userX} cy={MID_Y} r="3"  fill="#FEF3C7" />

      {/* User label above */}
      <text x={userX} y={MID_Y - HALF - 10} fill="#F59E0B" fontSize="10"
        textAnchor={userLabelSide} fontWeight="700">Tú</text>

      {/* Median label below */}
      <text x={medX} y={MID_Y + HALF + 14} fill="#10B981" fontSize="9" textAnchor="middle">mediana</text>

      {/* Min / Max labels */}
      <text x={sx(stats.min)} y={H - 2} fill="#6B7280" fontSize="9" textAnchor="middle">
        {Math.round(stats.min).toLocaleString()}
      </text>
      <text x={sx(stats.max)} y={H - 2} fill="#6B7280" fontSize="9" textAnchor="middle">
        {Math.round(stats.max).toLocaleString()}
      </text>
    </svg>
  );
}

export default function ProgressPage() {
  const user = getStoredUser();
  const [stats, setStats] = useState<ProgressStats | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/users/progress-stats")
      .then((r) => setStats(r.data))
      .finally(() => setLoading(false));
  }, []);

  if (!user) return null;

  const currentLevel = LEVELS_DATA.find((l) => l.level === user.level) ?? LEVELS_DATA[0];
  const nextLevel = LEVELS_DATA.find((l) => l.level === user.level + 1);
  const levelMin = currentLevel.minXp;
  const levelMax = currentLevel.maxXp ?? levelMin + 10000;
  const levelPct = Math.min(100, Math.round(((user.xp - levelMin) / (levelMax - levelMin)) * 100));
  const xpToNext = nextLevel ? Math.max(0, nextLevel.minXp - user.xp) : 0;

  const percentileMessage =
    !stats ? "" :
    stats.user_percentile >= 75 ? "¡Estás en el cuartil superior del curso!" :
    stats.user_percentile >= 50 ? "Estás sobre la mediana del curso." :
    stats.user_percentile >= 25 ? "Estás en el segundo cuartil — sigue sumando XP." :
    "Tienes mucho espacio para crecer — ¡a formular!";

  return (
    <div className="space-y-8 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold">📈 Tu Progreso</h1>
        <p className="text-foreground-muted text-sm mt-1">Tu posición en el curso y tu camino hacia el nivel máximo</p>
      </div>

      {/* Percentile hero */}
      {loading ? (
        <div className="card h-28 animate-pulse bg-surface-2" />
      ) : stats && (
        <div className="card">
          <div className="flex flex-col sm:flex-row items-center sm:items-start gap-6">
            <div className="text-center shrink-0">
              <p className="text-6xl font-bold tabular-nums text-primary">{stats.user_percentile}</p>
              <p className="text-sm text-foreground-muted mt-0.5">percentil</p>
            </div>
            <div className="flex-1 text-center sm:text-left">
              <p className="text-lg font-semibold">{percentileMessage}</p>
              <p className="text-foreground-muted text-sm mt-1">
                Superando al {stats.user_percentile}% de tus compañeros ·{" "}
                {stats.count} {stats.count === 1 ? "estudiante" : "estudiantes"} en el curso
              </p>
              <div className="flex flex-wrap gap-4 mt-3 justify-center sm:justify-start">
                <span className="text-accent font-mono font-bold text-lg">{user.xp.toLocaleString()} XP</span>
                <span className="text-foreground-muted text-sm self-center">
                  Promedio del curso:{" "}
                  <span className="text-foreground font-medium">{Math.round(stats.mean).toLocaleString()} XP</span>
                </span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Boxplot */}
      <div className="card">
        <h2 className="font-semibold mb-1">Distribución de XP del curso</h2>
        <p className="text-foreground-muted text-xs mb-5">
          El rectángulo azul agrupa al 50% central (Q1–Q3). La línea verde es la mediana.
          El punto naranja eres tú.
        </p>
        {loading ? (
          <div className="h-28 animate-pulse bg-surface-2 rounded-xl" />
        ) : stats ? (
          <>
            <BoxPlot stats={stats} />
            <div className="grid grid-cols-2 sm:grid-cols-5 gap-3 mt-5">
              {[
                { label: "Mínimo",    value: stats.min,    color: "text-foreground-muted" },
                { label: "Q1 (25%)", value: stats.q1,    color: "text-foreground-muted" },
                { label: "Mediana",   value: stats.median, color: "text-accent" },
                { label: "Q3 (75%)", value: stats.q3,    color: "text-foreground-muted" },
                { label: "Máximo",    value: stats.max,    color: "text-primary" },
              ].map((s) => (
                <div key={s.label} className="bg-surface-2 rounded-xl p-3 text-center">
                  <p className={`text-lg font-bold font-mono ${s.color}`}>
                    {Math.round(s.value).toLocaleString()}
                  </p>
                  <p className="text-xs text-foreground-muted mt-0.5">{s.label}</p>
                </div>
              ))}
            </div>
            <div className="flex items-center gap-6 mt-4 text-xs text-foreground-muted">
              <span className="flex items-center gap-1.5">
                <span className="inline-block w-4 h-0.5 bg-accent-warn rounded" />
                Tú
              </span>
              <span className="flex items-center gap-1.5">
                <span className="inline-block w-4 h-0.5 bg-accent rounded" />
                Mediana
              </span>
              <span className="flex items-center gap-1.5">
                <span className="inline-block w-4 h-px bg-foreground-muted/50 border-dashed border-t" />
                Promedio
              </span>
              <span className="flex items-center gap-1.5">
                <span className="inline-block w-4 h-3 rounded border border-primary bg-primary/10" />
                50% central
              </span>
            </div>
          </>
        ) : null}
      </div>

      {/* Level roadmap */}
      <div className="card">
        <h2 className="font-semibold mb-5">Camino de niveles</h2>

        {/* Progress to next level */}
        <div className="mb-8 p-4 bg-surface-2 rounded-2xl">
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-semibold">
              {LEVEL_NAMES[user.level]}
              {nextLevel && <span className="text-foreground-muted font-normal"> → {LEVEL_NAMES[nextLevel.level]}</span>}
            </span>
            <span className="text-sm text-accent font-mono">
              {user.xp.toLocaleString()} / {levelMax.toLocaleString()} XP
            </span>
          </div>
          <div className="h-3 bg-surface rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-primary to-primary-light rounded-full transition-all duration-700"
              style={{ width: `${levelPct}%` }}
            />
          </div>
          <p className="text-xs text-foreground-muted mt-2">
            {nextLevel
              ? `Te faltan ${xpToNext.toLocaleString()} XP para alcanzar ${LEVEL_NAMES[nextLevel.level]}`
              : "🏆 ¡Alcanzaste el nivel máximo!"}
          </p>
        </div>

        {/* Steps */}
        <div className="relative">
          <div className="hidden sm:block absolute top-5 left-10 right-10 h-px bg-border" />
          <div className="grid grid-cols-3 sm:grid-cols-6 gap-y-6 gap-x-2 relative">
            {LEVELS_DATA.map((lvl) => {
              const isCurrent = lvl.level === user.level;
              const isDone = lvl.level < user.level;
              return (
                <div key={lvl.level} className="flex flex-col items-center gap-2">
                  <div className={`w-10 h-10 rounded-2xl flex items-center justify-center text-xl border-2 relative z-10 transition-all ${
                    isCurrent
                      ? "bg-primary/20 border-primary shadow-md shadow-primary/20 scale-110"
                      : isDone
                      ? "bg-accent/15 border-accent/40"
                      : "bg-surface-2 border-border opacity-35"
                  }`}>
                    {lvl.icon}
                  </div>
                  <div className="text-center">
                    <p className={`text-xs font-semibold leading-tight ${
                      isCurrent ? "text-primary" : isDone ? "text-accent" : "text-foreground-muted"
                    }`}>
                      {lvl.name}
                    </p>
                    <p className="text-xs text-foreground-muted/60 leading-tight mt-0.5">
                      {lvl.maxXp
                        ? `${(lvl.minXp / 1000).toFixed(lvl.minXp < 1000 ? 0 : 1)}k–${(lvl.maxXp / 1000).toFixed(1)}k`
                        : `${(lvl.minXp / 1000).toFixed(0)}k+`}
                    </p>
                  </div>
                  {isCurrent && (
                    <span className="text-xs bg-primary/20 text-primary font-medium px-1.5 py-0.5 rounded-full">aquí</span>
                  )}
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}
