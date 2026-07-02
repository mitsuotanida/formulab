"use client";
import { useEffect, useState } from "react";
import api from "@/lib/api";
import { getStoredUser } from "@/lib/auth";
import { LEVEL_NAMES, BADGE_NAMES, type Badge } from "@/lib/types";
import { clsx } from "clsx";

export default function ProfilePage() {
  const [user, setUser] = useState(getStoredUser());
  const [badges, setBadges] = useState<Badge[]>([]);
  const [loading, setLoading] = useState(true);
  const [editingNickname, setEditingNickname] = useState(false);
  const [newNickname, setNewNickname] = useState(user?.nickname || "");
  const [savingNickname, setSavingNickname] = useState(false);

  useEffect(() => {
    api.get("/badges").then((b) => setBadges(b.data)).finally(() => setLoading(false));
  }, []);

  async function saveNickname() {
    setSavingNickname(true);
    try {
      await api.patch("/users/me", { nickname: newNickname.trim() });
      const stored = getStoredUser();
      if (stored) {
        stored.nickname = newNickname.trim() || undefined;
        localStorage.setItem("formulab_user", JSON.stringify(stored));
        setUser({ ...stored });
      }
      setEditingNickname(false);
    } finally {
      setSavingNickname(false);
    }
  }

  if (!user) return null;

  return (
    <div className="space-y-8 animate-fade-in">
      <div className="card flex flex-col sm:flex-row items-center sm:items-start gap-4 sm:gap-6">
        <div className="w-20 h-20 shrink-0 rounded-2xl bg-primary/20 border border-primary/30 flex items-center justify-center text-4xl font-bold text-primary">
          {(user.nickname || user.name)[0].toUpperCase()}
        </div>
        <div className="flex-1 text-center sm:text-left">
          <h1 className="text-2xl font-bold">{user.name}</h1>

          <div className="mt-1 flex items-center gap-2 justify-center sm:justify-start flex-wrap">
            {editingNickname ? (
              <>
                <input
                  autoFocus
                  value={newNickname}
                  onChange={(e) => setNewNickname(e.target.value)}
                  maxLength={30}
                  placeholder="Tu apodo..."
                  className="input text-sm py-1.5 px-3 w-36"
                  onKeyDown={(e) => e.key === "Enter" && saveNickname()}
                />
                <button onClick={saveNickname} disabled={savingNickname} className="btn-primary text-xs py-1.5 px-3">
                  {savingNickname ? "..." : "Guardar"}
                </button>
                <button
                  onClick={() => { setEditingNickname(false); setNewNickname(user.nickname || ""); }}
                  className="text-xs text-foreground-muted hover:text-foreground transition-colors"
                >
                  Cancelar
                </button>
              </>
            ) : (
              <>
                {user.nickname ? (
                  <span className="text-primary font-medium text-sm">"{user.nickname}"</span>
                ) : (
                  <span className="text-foreground-muted text-sm italic">Sin apodo</span>
                )}
                <button
                  onClick={() => setEditingNickname(true)}
                  className="text-xs text-foreground-muted hover:text-primary transition-colors underline underline-offset-2"
                >
                  {user.nickname ? "Cambiar" : "Agregar apodo"}
                </button>
              </>
            )}
          </div>

          <p className="text-foreground-muted text-sm mt-1">{user.email}</p>
          <div className="flex flex-wrap justify-center sm:justify-start gap-3 sm:gap-4 mt-2">
            <span className="text-primary font-semibold">{LEVEL_NAMES[user.level]}</span>
            <span className="text-accent font-mono">{user.xp.toLocaleString()} XP</span>
            <span className="text-accent-warn">🔥 {user.streak} días</span>
          </div>
        </div>
      </div>

      <div className="card">
        <h2 className="font-semibold mb-4">Insignias</h2>
        {loading ? (
          <div className="h-48 animate-pulse bg-surface-2 rounded" />
        ) : badges.length === 0 ? (
          <p className="text-foreground-muted text-sm">Completa ejercicios para desbloquear insignias.</p>
        ) : (
          <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-6 gap-3">
            {badges.map((b) => (
              <div key={b.id} className={clsx("flex flex-col items-center gap-1 p-3 rounded-xl border transition-all",
                b.earned ? "bg-accent/10 border-accent/30" : "bg-surface-2 border-border opacity-40 grayscale"
              )}>
                <span className="text-2xl">{b.earned ? "🏅" : "🔒"}</span>
                <p className="text-xs text-center font-medium leading-tight">{BADGE_NAMES[b.name] ?? b.name}</p>
                {b.earned && <p className="text-xs text-accent">+{b.xp_reward} XP</p>}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
