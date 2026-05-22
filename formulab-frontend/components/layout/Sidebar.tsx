"use client";
import { useState } from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { getStoredUser, clearSession } from "@/lib/auth";
import { LEVEL_NAMES } from "@/lib/types";
import { clsx } from "clsx";

const NAV_ITEMS = [
  { href: "/dashboard", label: "Dashboard", icon: "⚡" },
  { href: "/exercises", label: "Ejercicios", icon: "📐" },
  { href: "/leaderboard", label: "Ranking", icon: "🏆" },
  { href: "/profile", label: "Mi Perfil", icon: "🎖️" },
];

const ADMIN_ITEMS = [
  { href: "/admin", label: "Panel Admin", icon: "🛠️" },
  { href: "/admin/exercises", label: "Gestionar ejercicios", icon: "📋" },
  { href: "/admin/students", label: "Estudiantes", icon: "👥" },
  { href: "/admin/analytics", label: "Analítica", icon: "📊" },
];

export default function Sidebar() {
  const pathname = usePathname();
  const router = useRouter();
  const user = getStoredUser();
  const [mobileOpen, setMobileOpen] = useState(false);

  function handleLogout() {
    clearSession();
    router.replace("/login");
  }

  function close() {
    setMobileOpen(false);
  }

  return (
    <>
      {/* ── Mobile top bar (hidden on md+) ──────────────────── */}
      <header className="fixed top-0 left-0 right-0 h-14 bg-surface border-b border-border flex items-center gap-3 px-4 z-30 md:hidden">
        <button
          onClick={() => setMobileOpen(true)}
          className="p-2 rounded-lg hover:bg-surface-2 transition-colors"
          aria-label="Abrir menú"
        >
          <svg width="20" height="20" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
            <line x1="2" y1="4" x2="18" y2="4" />
            <line x1="2" y1="10" x2="18" y2="10" />
            <line x1="2" y1="16" x2="18" y2="16" />
          </svg>
        </button>
        <div className="flex items-center gap-2">
          <div className="w-7 h-7 rounded-lg bg-primary/20 border border-primary/30 flex items-center justify-center text-sm">⚡</div>
          <span className="font-bold text-sm">FormuLab</span>
        </div>
        {user && (
          <div className="ml-auto text-right">
            <p className="text-xs font-medium leading-none">{user.name.split(" ")[0]}</p>
            <p className="text-xs text-accent font-mono mt-0.5">{user.xp.toLocaleString()} XP</p>
          </div>
        )}
      </header>

      {/* ── Backdrop (mobile only) ───────────────────────────── */}
      {mobileOpen && (
        <div
          className="fixed inset-0 bg-black/60 z-40 md:hidden"
          onClick={close}
        />
      )}

      {/* ── Sidebar ─────────────────────────────────────────── */}
      <aside
        className={clsx(
          "fixed left-0 top-0 w-64 h-screen bg-surface border-r border-border flex flex-col z-50 transition-transform duration-300",
          "md:translate-x-0",
          mobileOpen ? "translate-x-0" : "-translate-x-full"
        )}
      >
        {/* Header */}
        <div className="p-6 border-b border-border flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-primary/20 border border-primary/30 flex items-center justify-center text-xl">⚡</div>
            <div>
              <h1 className="font-bold text-lg">FormuLab</h1>
              <p className="text-xs text-foreground-muted">CII 2750 · UDP</p>
            </div>
          </div>
          <button
            onClick={close}
            className="md:hidden w-8 h-8 flex items-center justify-center rounded-lg hover:bg-surface-2 text-foreground-muted transition-colors"
            aria-label="Cerrar menú"
          >
            <svg width="16" height="16" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round">
              <line x1="2" y1="2" x2="14" y2="14" />
              <line x1="14" y1="2" x2="2" y2="14" />
            </svg>
          </button>
        </div>

        {/* User card */}
        {user && (
          <div className="px-4 py-4 border-b border-border">
            <div className="bg-surface-2 rounded-xl p-3">
              <p className="font-medium text-sm truncate">{user.name}</p>
              <div className="flex items-center gap-2 mt-1">
                <span className="text-xs text-primary font-medium">{LEVEL_NAMES[user.level] || "Intern"}</span>
                <span className="text-foreground-muted text-xs">·</span>
                <span className="text-xs text-accent font-mono">{user.xp.toLocaleString()} XP</span>
              </div>
            </div>
          </div>
        )}

        {/* Navigation */}
        <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
          {NAV_ITEMS.map((item) => (
            <Link
              key={item.href}
              href={item.href}
              onClick={close}
              className={clsx(
                "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all",
                pathname === item.href || pathname.startsWith(item.href + "/")
                  ? "bg-primary/20 text-primary border border-primary/30"
                  : "text-foreground-muted hover:bg-surface-2 hover:text-foreground"
              )}
            >
              <span className="text-base">{item.icon}</span>
              {item.label}
            </Link>
          ))}

          {user?.role === "teacher" && (
            <>
              <div className="pt-4 pb-2 px-3">
                <p className="text-xs text-foreground-muted font-medium uppercase tracking-wider">Profesor</p>
              </div>
              {ADMIN_ITEMS.map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  onClick={close}
                  className={clsx(
                    "flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all",
                    pathname === item.href
                      ? "bg-accent-warn/20 text-accent-warn border border-accent-warn/30"
                      : "text-foreground-muted hover:bg-surface-2 hover:text-foreground"
                  )}
                >
                  <span className="text-base">{item.icon}</span>
                  {item.label}
                </Link>
              ))}
            </>
          )}
        </nav>

        {/* Logout */}
        <div className="p-4 border-t border-border">
          <button
            onClick={handleLogout}
            className="w-full text-left flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-foreground-muted hover:text-destructive hover:bg-destructive/10 transition-all"
          >
            <span>🚪</span> Cerrar sesión
          </button>
        </div>
      </aside>
    </>
  );
}
