"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import api from "@/lib/api";
import { DIFFICULTY_LABELS, DOMAIN_LABELS, TYPE_LABELS, type Exercise } from "@/lib/types";

export default function AdminExercisesPage() {
  const [exercises, setExercises] = useState<Exercise[]>([]);
  const [loading, setLoading] = useState(true);
  const [generating, setGenerating] = useState(false);
  const [genForm, setGenForm] = useState({ type: "LP", domain: "production", difficulty: "medium", custom_context: "" });
  const [showGen, setShowGen] = useState(false);

  function load() {
    api.get("/exercises?per_page=50").then((r) => setExercises(r.data.data)).finally(() => setLoading(false));
  }
  useEffect(load, []);

  async function handleGenerate() {
    setGenerating(true);
    try {
      await api.post("/exercises/generate", { ...genForm, ra_focus: [] });
      setShowGen(false);
      load();
    } finally { setGenerating(false); }
  }

  async function handleDeactivate(id: string) {
    if (!confirm("¿Desactivar este ejercicio?")) return;
    await api.delete(`/exercises/${id}`);
    load();
  }

  return (
    <div className="space-y-6 animate-fade-in">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">📋 Gestionar Ejercicios</h1>
        <button onClick={() => setShowGen(!showGen)} className="btn-primary text-sm">✨ Generar con IA</button>
      </div>

      {showGen && (
        <div className="card border-primary/30 bg-primary/5 space-y-4">
          <h3 className="font-semibold">Generador de Ejercicios con IA</h3>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
            {[
              { label: "Tipo", key: "type", options: [["LP", "Prog. Lineal"], ["MIP", "Prog. Entera Mixta"], ["NLP", "Prog. No Lineal"]] },
              { label: "Dominio", key: "domain", options: Object.entries(DOMAIN_LABELS) },
              { label: "Dificultad", key: "difficulty", options: [["easy", "Fácil"], ["medium", "Medio"], ["hard", "Difícil"]] },
            ].map((field) => (
              <div key={field.key}>
                <label className="text-sm text-foreground-muted mb-1.5 block">{field.label}</label>
                <select value={genForm[field.key as keyof typeof genForm]} onChange={(e) => setGenForm({ ...genForm, [field.key]: e.target.value })} className="input">
                  {field.options.map(([v, l]) => <option key={v} value={v}>{l}</option>)}
                </select>
              </div>
            ))}
          </div>
          <div>
            <label className="text-sm text-foreground-muted mb-1.5 block">Contexto adicional (opcional)</label>
            <input type="text" value={genForm.custom_context} onChange={(e) => setGenForm({ ...genForm, custom_context: e.target.value })} placeholder="Ej: industria del salmón chileno" className="input" />
          </div>
          <button onClick={handleGenerate} disabled={generating} className="btn-primary">
            {generating ? "⏳ Generando con Claude..." : "⚡ Generar ejercicio"}
          </button>
        </div>
      )}

      <div className="card p-0 overflow-x-auto">
        <table className="w-full text-sm min-w-[640px]">
          <thead>
            <tr className="border-b border-border">
              {["Título", "Tipo", "Dificultad", "Dominio", "RAs", "Fuente", "Acciones"].map((h) => (
                <th key={h} className="text-left px-4 py-3 text-xs text-foreground-muted uppercase tracking-wider">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {loading ? [...Array(5)].map((_, i) => <tr key={i}><td colSpan={7} className="px-4 py-4"><div className="h-4 bg-surface-2 rounded animate-pulse" /></td></tr>) :
              exercises.map((ex) => (
                <tr key={ex.id} className="border-b border-border last:border-0 hover:bg-surface-2 transition-colors">
                  <td className="px-4 py-3 max-w-xs">
                    <p className="font-medium text-xs truncate">{ex.title}</p>
                  </td>
                  <td className="px-4 py-3"><span className="badge-type">{ex.type}</span></td>
                  <td className="px-4 py-3"><span className={`badge-difficulty-${ex.difficulty}`}>{DIFFICULTY_LABELS[ex.difficulty]}</span></td>
                  <td className="px-4 py-3 text-xs text-foreground-muted">{DOMAIN_LABELS[ex.domain]}</td>
                  <td className="px-4 py-3 text-xs text-foreground-muted">{ex.ra_ids.join(", ")}</td>
                  <td className="px-4 py-3">{ex.ai_generated ? <span className="text-purple-400 text-xs">IA</span> : <span className="text-foreground-muted text-xs">Manual</span>}</td>
                  <td className="px-4 py-3">
                    <button onClick={() => handleDeactivate(ex.id)} className="text-xs text-destructive hover:text-destructive/80 transition-colors">Desactivar</button>
                  </td>
                </tr>
              ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
