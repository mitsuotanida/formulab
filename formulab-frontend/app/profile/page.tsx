"use client";
import { useEffect, useState } from "react";
import api from "@/lib/api";
import { getStoredUser } from "@/lib/auth";
import { LEVEL_NAMES, type Badge, type RATracking } from "@/lib/types";
import { RadarChart, PolarGrid, PolarAngleAxis, Radar, ResponsiveContainer } from "recharts";
import { clsx } from "clsx";

export default function ProfilePage() {
  const user = getStoredUser();
  const [badges, setBadges] = useState<Badge[]>([]);
  const [raData, setRaData] = useState<RATracking[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([api.get("/badges"), api.get("/ra-tracking/me")]).then(([b, r]) => {
      setBadges(b.data);
      setRaData(r.data.data);
    }).finally(() => setLoading(false));
  }, []);

  if (!user) return null;

  const raChartData = raData.map((r) => ({
    ra: `RA${r.ra_id}`,
    value: Math.round(r.success_rate * 100),
    full: 100,
  }));

  return (
    <div className="space-y-8 animate-fade-in">
      <div className="card flex items-center gap-6">
        <div className="w-20 h-20 rounded-2xl bg-primary/20 border border-primary/30 flex items-center justify-center text-4xl font-bold text-primary">
          {user.name[0].toUpperCase()}
        </div>
        <div className="flex-1">
          <h1 className="text-2xl font-bold">{user.name}</h1>
          <p className="text-foreground-muted">{user.email}</p>
          <div className="flex gap-4 mt-2">
            <span className="text-primary font-semibold">{LEVEL_NAMES[user.level]}</span>
            <span className="text-accent font-mono">{user.xp.toLocaleString()} XP</span>
            <span className="text-accent-warn">🔥 {user.streak} días</span>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="font-semibold mb-4">Resultados de Aprendizaje</h2>
          {loading ? <div className="h-48 animate-pulse bg-surface-2 rounded" /> : raChartData.length > 0 ? (
            <ResponsiveContainer width="100%" height={220}>
              <RadarChart data={raChartData}>
                <PolarGrid stroke="#2A2A3D" />
                <PolarAngleAxis dataKey="ra" tick={{ fill: "#9CA3AF", fontSize: 12 }} />
                <Radar dataKey="value" stroke="#6366F1" fill="#6366F1" fillOpacity={0.2} />
              </RadarChart>
            </ResponsiveContainer>
          ) : <p className="text-foreground-muted text-sm">Completa ejercicios para ver tu progreso por RA.</p>}
          <div className="space-y-2 mt-4">
            {raData.map((r) => (
              <div key={r.ra_id} className="flex items-center gap-3">
                <span className="text-xs text-foreground-muted w-8">RA{r.ra_id}</span>
                <div className="flex-1 h-1.5 bg-surface-2 rounded-full overflow-hidden">
                  <div className="h-full bg-primary rounded-full" style={{ width: `${r.success_rate * 100}%` }} />
                </div>
                <span className="text-xs text-foreground-muted w-10 text-right">{Math.round(r.success_rate * 100)}%</span>
              </div>
            ))}
          </div>
        </div>

        <div className="card">
          <h2 className="font-semibold mb-4">Insignias</h2>
          {loading ? <div className="h-48 animate-pulse bg-surface-2 rounded" /> : (
            <div className="grid grid-cols-3 gap-3">
              {badges.map((b) => (
                <div key={b.id} className={clsx("flex flex-col items-center gap-1 p-3 rounded-xl border transition-all",
                  b.earned ? "bg-accent/10 border-accent/30" : "bg-surface-2 border-border opacity-40 grayscale"
                )}>
                  <span className="text-2xl">{b.earned ? "🏅" : "🔒"}</span>
                  <p className="text-xs text-center font-medium leading-tight">{b.name}</p>
                  {b.earned && <p className="text-xs text-accent">+{b.xp_reward} XP</p>}
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
