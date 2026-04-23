"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import api from "@/lib/api";
import { DIFFICULTY_LABELS, DOMAIN_LABELS, TYPE_LABELS, type Exercise } from "@/lib/types";
import { clsx } from "clsx";

const TYPES = ["LP", "MIP", "NLP"];
const DIFFICULTIES = ["easy", "medium", "hard"];
const DOMAINS = ["production", "logistics", "agriculture", "finance", "inventory", "energy", "generic"];

export default function ExercisesPage() {
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [total, setTotal] = useState(0);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({ type: "", difficulty: "", domain: "" });
  const [page, setPage] = useState(1);

  useEffect(() => {
    setLoading(true);
    const params = new URLSearchParams({ page: String(page), per_page: "12" });
    if (filters.type) params.set("type", filters.type);
    if (filters.difficulty) params.set("difficulty", filters.difficulty);
    if (filters.domain) params.set("domain", filters.domain);
    api.get(`/exercises?${params}`).then((r) => {
      setExercises(r.data.data);
      setTotal(r.data.total);
    }).finally(() => setLoading(false));
  }, [filters, page]);

  function setFilter(key: string, val: string) {
    setFilters((f) => ({ ...f, [key]: f[key as keyof typeof f] === val ? "" : val }));
    setPage(1);
  }

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold">Ejercicios</h1>
          <p className="text-foreground-muted text-sm mt-1">{total} ejercicios disponibles</p>
        </div>
      </div>

      <div className="card space-y-4">
        <div>
          <p className="text-xs text-foreground-muted uppercase tracking-wider mb-2">Tipo de modelo</p>
          <div className="flex gap-2 flex-wrap">
            {TYPES.map((t) => (
              <button key={t} onClick={() => setFilter("type", t)}
                className={clsx("px-3 py-1.5 rounded-lg text-sm font-medium border transition-all",
                  filters.type === t ? "bg-primary/20 border-primary text-primary" : "border-border text-foreground-muted hover:border-primary/50"
                )}>
                {TYPE_LABELS[t]}
              </button>
            ))}
          </div>
        </div>
        <div>
          <p className="text-xs text-foreground-muted uppercase tracking-wider mb-2">Dificultad</p>
          <div className="flex gap-2">
            {DIFFICULTIES.map((d) => (
              <button key={d} onClick={() => setFilter("difficulty", d)}
                className={clsx("px-3 py-1.5 rounded-lg text-sm font-medium border transition-all",
                  filters.difficulty === d ? "bg-surface-2 border-foreground text-foreground" : "border-border text-foreground-muted hover:border-foreground/50"
                )}>
                {DIFFICULTY_LABELS[d]}
              </button>
            ))}
          </div>
        </div>
        <div>
          <p className="text-xs text-foreground-muted uppercase tracking-wider mb-2">Dominio</p>
          <div className="flex gap-2 flex-wrap">
            {DOMAINS.map((d) => (
              <button key={d} onClick={() => setFilter("domain", d)}
                className={clsx("px-3 py-1.5 rounded-lg text-sm font-medium border transition-all",
                  filters.domain === d ? "bg-surface-2 border-foreground text-foreground" : "border-border text-foreground-muted hover:border-foreground/50"
                )}>
                {DOMAIN_LABELS[d]}
              </button>
            ))}
          </div>
        </div>
      </div>

      {loading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {[...Array(6)].map((_, i) => <div key={i} className="card h-40 animate-pulse bg-surface-2" />)}
        </div>
      ) : exercises.length === 0 ? (
        <div className="text-center py-16 text-foreground-muted">
          <p className="text-4xl mb-3">📭</p>
          <p>No se encontraron ejercicios con estos filtros</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {exercises.map((ex) => (
            <Link key={ex.id} href={`/exercises/${ex.id}`} className="card-hover block space-y-3">
              <div className="flex items-start justify-between gap-2">
                <h3 className="font-medium text-sm line-clamp-2 flex-1">{ex.title}</h3>
                {ex.user_best_score != null && (
                  <div className={clsx("text-xs font-bold shrink-0 rounded-full w-8 h-8 flex items-center justify-center",
                    ex.user_best_score >= 70 ? "bg-accent/20 text-accent" : "bg-accent-warn/20 text-accent-warn"
                  )}>
                    {ex.user_best_score}
                  </div>
                )}
              </div>
              <p className="text-xs text-foreground-muted line-clamp-2">{ex.description}</p>
              <div className="flex gap-2 flex-wrap pt-1">
                <span className="badge-type">{TYPE_LABELS[ex.type]}</span>
                <span className={`badge-difficulty-${ex.difficulty}`}>{DIFFICULTY_LABELS[ex.difficulty]}</span>
                {ex.ai_generated && <span className="bg-purple-500/20 text-purple-400 text-xs font-medium px-2.5 py-1 rounded-full">IA</span>}
              </div>
              <div className="flex items-center justify-between text-xs text-foreground-muted pt-1">
                <span>{DOMAIN_LABELS[ex.domain]}</span>
                <span>{ex.hints_count} pistas · {ex.user_attempts} intentos</span>
              </div>
            </Link>
          ))}
        </div>
      )}

      {total > 12 && (
        <div className="flex justify-center gap-2">
          <button onClick={() => setPage((p) => Math.max(1, p - 1))} disabled={page === 1} className="btn-secondary px-4 py-2 text-sm disabled:opacity-40">← Anterior</button>
          <span className="px-4 py-2 text-sm text-foreground-muted">Página {page}</span>
          <button onClick={() => setPage((p) => p + 1)} disabled={page * 12 >= total} className="btn-secondary px-4 py-2 text-sm disabled:opacity-40">Siguiente →</button>
        </div>
      )}
    </div>
  );
}
