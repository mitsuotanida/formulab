"use client";
import { useEffect, useState } from "react";
import api from "@/lib/api";
import { LEVEL_NAMES, type LeaderboardEntry } from "@/lib/types";
import { clsx } from "clsx";
import { getStoredUser } from "@/lib/auth";

export default function LeaderboardPage() {
  const [entries, setEntries] = useState<LeaderboardEntry[]>([]);
  const [period, setPeriod] = useState<"all_time" | "weekly">("all_time");
  const [loading, setLoading] = useState(true);
  const me = getStoredUser();

  useEffect(() => {
    setLoading(true);
    api.get(`/users/leaderboard?period=${period}&per_page=30`).then((r) => setEntries(r.data.data)).finally(() => setLoading(false));
  }, [period]);

  const medals = ["🥇", "🥈", "🥉"];

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">🏆 Ranking</h1>
          <p className="text-foreground-muted text-sm mt-1">Tabla de posiciones de FormuLab</p>
        </div>
        <div className="flex gap-2">
          {(["all_time", "weekly"] as const).map((p) => (
            <button key={p} onClick={() => setPeriod(p)}
              className={clsx("px-4 py-2 rounded-lg text-sm font-medium border transition-all",
                period === p ? "bg-primary/20 border-primary text-primary" : "border-border text-foreground-muted hover:border-primary/50"
              )}>
              {p === "all_time" ? "Todo el tiempo" : "Esta semana"}
            </button>
          ))}
        </div>
      </div>

      {loading ? (
        <div className="space-y-3">
          {[...Array(8)].map((_, i) => <div key={i} className="card h-16 animate-pulse bg-surface-2" />)}
        </div>
      ) : (
        <div className="card p-0 overflow-hidden">
          {entries.map((entry, i) => (
            <div key={entry.user_id} className={clsx(
              "flex items-center gap-4 px-6 py-4 border-b border-border last:border-0 transition-colors",
              entry.user_id === me?.id ? "bg-primary/5" : "hover:bg-surface-2"
            )}>
              <div className="w-8 text-center">
                {i < 3 ? <span className="text-xl">{medals[i]}</span> : <span className="text-foreground-muted font-mono text-sm">{entry.rank}</span>}
              </div>
              <div className="w-10 h-10 rounded-full bg-primary/20 flex items-center justify-center text-lg font-bold text-primary shrink-0">
                {entry.name[0].toUpperCase()}
              </div>
              <div className="flex-1 min-w-0">
                <p className="font-medium truncate">{entry.name} {entry.user_id === me?.id && <span className="text-xs text-primary">(tú)</span>}</p>
                <p className="text-xs text-foreground-muted">{LEVEL_NAMES[entry.level]} · {entry.exercises_completed} ejercicios completados</p>
              </div>
              <div className="text-right shrink-0">
                <p className="font-bold font-mono text-accent">{entry.xp.toLocaleString()}</p>
                <p className="text-xs text-foreground-muted">XP</p>
              </div>
              {entry.streak > 0 && (
                <div className="text-right shrink-0">
                  <p className="text-accent-warn font-medium text-sm">🔥 {entry.streak}</p>
                </div>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
