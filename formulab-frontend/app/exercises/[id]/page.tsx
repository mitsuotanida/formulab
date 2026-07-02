"use client";
import { useEffect, useState, useRef, useMemo } from "react";
import { useParams } from "next/navigation";
import api from "@/lib/api";
import { DIFFICULTY_LABELS, DOMAIN_LABELS, TYPE_LABELS, type Exercise, type Submission } from "@/lib/types";
import { clsx } from "clsx";
import katex from "katex";
import "katex/dist/katex.min.css";

function escapeHtml(text: string) {
  return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function renderLatexToHtml(input: string): string {
  const parts = input.split(/(\$\$[\s\S]*?\$\$|\$[^$\n]+?\$)/g);
  return parts.map((part) => {
    if (part.startsWith("$$") && part.endsWith("$$") && part.length > 4) {
      const math = part.slice(2, -2);
      try {
        return `<div class="katex-display-wrap my-2 overflow-x-auto">${katex.renderToString(math, { displayMode: true, throwOnError: false })}</div>`;
      } catch {
        return `<span class="text-red-400 text-xs font-mono">[Error: ${escapeHtml(math)}]</span>`;
      }
    }
    if (part.startsWith("$") && part.endsWith("$") && part.length > 2) {
      const math = part.slice(1, -1);
      try {
        return katex.renderToString(math, { displayMode: false, throwOnError: false });
      } catch {
        return `<span class="text-red-400 text-xs font-mono">[Error: ${escapeHtml(math)}]</span>`;
      }
    }
    return escapeHtml(part).replace(/\n/g, "<br/>");
  }).join("");
}

function ScoreRing({ score }: { score: number }) {
  const r = 45;
  const circ = 2 * Math.PI * r;
  const offset = circ - (score / 100) * circ;
  const color = score >= 80 ? "#10B981" : score >= 60 ? "#F59E0B" : "#EF4444";
  return (
    <div className="relative flex items-center justify-center w-32 h-32">
      <svg width="128" height="128" className="-rotate-90">
        <circle cx="64" cy="64" r={r} fill="none" stroke="#2A2A3D" strokeWidth="8" />
        <circle cx="64" cy="64" r={r} fill="none" stroke={color} strokeWidth="8" strokeDasharray={circ} strokeDashoffset={offset} strokeLinecap="round" style={{ transition: "stroke-dashoffset 1s ease" }} />
      </svg>
      <div className="absolute text-center">
        <p className="text-2xl font-bold" style={{ color }}>{score}</p>
        <p className="text-xs text-foreground-muted">/ 100</p>
      </div>
    </div>
  );
}

function DataTable({ table }: { table: { headers: string[]; rows: string[][] } }) {
  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm border-collapse">
        <thead>
          <tr>
            {table.headers.map((h, i) => (
              <th key={i} className="text-left px-4 py-2.5 bg-surface-2 border border-border text-foreground-muted font-medium">{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {table.rows.map((row, ri) => (
            <tr key={ri}>
              {row.map((cell, ci) => (
                <td key={ci} className="px-4 py-2.5 border border-border text-foreground font-mono text-xs">{cell}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default function ExercisePage() {
  const { id } = useParams<{ id: string }>();
  const [exercise, setExercise] = useState<Exercise | null>(null);
  const [content, setContent] = useState("");
  const [submission, setSubmission] = useState<Submission | null>(null);
  const [submitting, setSubmitting] = useState(false);
  const [revealedHints, setRevealedHints] = useState<Array<{ order: number; text: string }>>([]);
  const [hintsUsed, setHintsUsed] = useState(0);
  const [startTime] = useState(Date.now());
  const [latexMode, setLatexMode] = useState(false);
  const pollRef = useRef<ReturnType<typeof setInterval> | null>(null);
  const renderedLatex = useMemo(() => renderLatexToHtml(content), [content]);

  useEffect(() => {
    api.get(`/exercises/${id}`).then((r) => setExercise(r.data));
    return () => { if (pollRef.current) clearInterval(pollRef.current); };
  }, [id]);

  async function revealHint(order: number) {
    try {
      const { data } = await api.get(`/exercises/${id}/hints?order=${order}`);
      setRevealedHints((h) => [...h, data]);
      setHintsUsed((n) => n + 1);
    } catch { /* hint not found */ }
  }

  async function handleSubmit() {
    if (!content.trim()) return;
    setSubmitting(true);
    const timeSpent = Math.round((Date.now() - startTime) / 1000);
    try {
      const { data } = await api.post("/submissions", {
        exercise_id: id,
        content,
        time_spent_sec: timeSpent,
        hints_used: hintsUsed,
      });
      const subId = data.submission_id;
      pollRef.current = setInterval(async () => {
        const { data: sub } = await api.get(`/submissions/${subId}`);
        if (sub.evaluation_status === "complete" || sub.evaluation_status === "error") {
          clearInterval(pollRef.current!);
          setSubmission(sub);
          setSubmitting(false);
        }
      }, 2000);
    } catch {
      setSubmitting(false);
    }
  }

  if (!exercise) {
    return <div className="flex items-center justify-center h-64 text-foreground-muted animate-pulse">Cargando ejercicio...</div>;
  }

  return (
    <div className="space-y-6 animate-fade-in max-w-4xl">
      <div className="flex items-start gap-4">
        <div className="flex-1">
          <div className="flex gap-2 flex-wrap mb-2">
            <span className="badge-type">{TYPE_LABELS[exercise.type]}</span>
            <span className={`badge-difficulty-${exercise.difficulty}`}>{DIFFICULTY_LABELS[exercise.difficulty]}</span>
            <span className="text-xs text-foreground-muted px-2.5 py-1">{DOMAIN_LABELS[exercise.domain]}</span>
            {exercise.ai_generated && <span className="bg-purple-500/20 text-purple-400 text-xs px-2.5 py-1 rounded-full">Generado por IA</span>}
          </div>
          <h1 className="text-xl font-bold">{exercise.title}</h1>
          <div className="flex flex-wrap gap-2 sm:gap-4 mt-2 text-xs text-foreground-muted">
            <span>RAs: {exercise.ra_ids.join(", ")}</span>
            <span>{exercise.hints_count} pistas disponibles</span>
          </div>
        </div>
      </div>

      <div className="card">
        <h2 className="font-semibold mb-3 text-sm uppercase tracking-wider text-foreground-muted">Enunciado</h2>
        <p className="text-foreground leading-relaxed whitespace-pre-line">{exercise.description}</p>
        {exercise.data_table && (
          <div className="mt-4">
            <DataTable table={exercise.data_table} />
          </div>
        )}
      </div>

      <div className="card bg-primary/5 border-primary/20">
        <p className="text-sm font-medium text-primary">📋 Pregunta</p>
        <p className="mt-2 text-foreground">Formule el modelo de programación matemática. Defina las <strong>variables de decisión</strong>, la <strong>función objetivo</strong> y todas las <strong>restricciones</strong>.</p>
      </div>

      {exercise.hints_count > 0 && (
        <div className="card">
          <h3 className="text-sm font-semibold mb-3 text-foreground-muted uppercase tracking-wider">Pistas</h3>
          <div className="space-y-3">
            {revealedHints.map((hint) => (
              <div key={hint.order} className="bg-accent-warn/10 border border-accent-warn/20 rounded-lg px-4 py-3 text-sm">
                <span className="text-accent-warn font-medium">Pista {hint.order}:</span> {hint.text}
              </div>
            ))}
            {[...Array(exercise.hints_count)].map((_, i) => {
              const order = i + 1;
              const revealed = revealedHints.some((h) => h.order === order);
              if (revealed) return null;
              return (
                <button key={order} onClick={() => revealHint(order)}
                  className="w-full text-left border border-dashed border-border rounded-lg px-4 py-3 text-sm text-foreground-muted hover:border-accent-warn/50 hover:text-accent-warn transition-all">
                  🔒 Revelar pista {order} <span className="text-xs">(costo: 15 XP)</span>
                </button>
              );
            })}
          </div>
        </div>
      )}

      <div className="card">
        <div className="flex items-center justify-between mb-3">
          <h3 className="text-sm font-semibold text-foreground-muted uppercase tracking-wider">Tu Formulación</h3>
          <div className="flex items-center gap-1 bg-surface-2 rounded-lg p-1">
            <button
              onClick={() => setLatexMode(false)}
              className={clsx("text-xs px-3 py-1.5 rounded-md font-medium transition-all", !latexMode ? "bg-surface text-foreground shadow-sm" : "text-foreground-muted hover:text-foreground")}
            >
              Texto
            </button>
            <button
              onClick={() => setLatexMode(true)}
              className={clsx("text-xs px-3 py-1.5 rounded-md font-medium transition-all flex items-center gap-1.5", latexMode ? "bg-primary/20 text-primary shadow-sm border border-primary/30" : "text-foreground-muted hover:text-foreground")}
            >
              <span className="font-mono font-bold">∑</span> LaTeX
            </button>
          </div>
        </div>

        {latexMode ? (
          <>
            <p className="text-xs text-foreground-muted mb-3">
              Usa <code className="bg-surface-2 px-1 rounded text-primary">$...$</code> para matemática en línea y{" "}
              <code className="bg-surface-2 px-1 rounded text-primary">$$...$$</code> para ecuaciones centradas.
            </p>
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-3">
              <div>
                <p className="text-xs text-foreground-muted mb-1.5 font-medium">Código LaTeX</p>
                <textarea
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  rows={18}
                  placeholder={`% Conjuntos
$I = \\{1,2\\}$: plantas
$J = \\{P,V,C\\}$: productos
$T = \\{1,2,3\\}$: períodos

% Parámetros
$c_{ij}$: costo de producir $j$ en planta $i$

% Variables de decisión
$x_{ijt} \\geq 0 \\quad \\forall i \\in I, j \\in J, t \\in T$
$y_{it} \\in \\{0,1\\} \\quad \\forall i \\in I, t \\in T$

% Función objetivo
$$\\min Z = \\sum_{i \\in I}\\sum_{j \\in J}\\sum_{t \\in T} c_{ij}\\,x_{ijt}$$

% Restricciones
$$\\sum_{j \\in J} r_{ij}\\,x_{ijt} \\leq \\text{Cap}_i \\cdot y_{it} \\quad \\forall i \\in I, t \\in T$$`}
                  className="input font-mono text-xs resize-none w-full"
                  disabled={submitting || submission?.evaluation_status === "complete"}
                />
              </div>
              <div>
                <p className="text-xs text-foreground-muted mb-1.5 font-medium">Vista previa</p>
                <div
                  className="bg-surface-2 rounded-xl border border-border p-4 text-sm leading-relaxed min-h-[18rem] overflow-x-auto"
                  dangerouslySetInnerHTML={{ __html: content ? renderedLatex : '<span class="text-foreground-muted/50 text-xs italic">La vista previa aparece aquí mientras escribes...</span>' }}
                />
              </div>
            </div>
          </>
        ) : (
          <>
            <p className="text-xs text-foreground-muted mb-3">Escribe tu modelo completo. Puedes usar notación matemática (ej: x₁, ≤, Σᵢ, ∀i∈I, Max, Min).</p>
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              rows={14}
              placeholder={`Conjuntos (si aplica):
I = {1,...,m}: descripción
J = {1,...,n}: descripción

Parámetros (si aplica):
cᵢⱼ = costo de ... para i∈I, j∈J

Variables de decisión:
xᵢⱼ ≥ 0: unidades de j en i   ∀i∈I, j∈J
yᵢ ∈ {0,1}: 1 si ...

Función objetivo:
Min Z = ΣᵢΣⱼ cᵢⱼ·xᵢⱼ  +  ...

Restricciones:
Σⱼ aᵢⱼ·xᵢⱼ ≤ bᵢ   ∀i∈I
xᵢⱼ ≥ 0, yᵢ ∈ {0,1}`}
              className="input font-mono text-sm resize-none"
              disabled={submitting || submission?.evaluation_status === "complete"}
            />
          </>
        )}

        {!submission && (
          <button
            onClick={handleSubmit}
            disabled={submitting || !content.trim()}
            className="btn-primary mt-4 w-full"
          >
            {submitting ? "⏳ Evaluando con IA..." : "📤 Enviar Formulación"}
          </button>
        )}
      </div>

      {submitting && (
        <div className="card text-center py-8">
          <div className="animate-spin text-4xl mb-4">⚙️</div>
          <p className="text-foreground font-medium">La IA está evaluando tu formulación...</p>
          <p className="text-foreground-muted text-sm mt-1">Esto tarda entre 5 y 15 segundos</p>
        </div>
      )}

      {submission && submission.evaluation_status === "complete" && submission.feedback && (
        <div className="space-y-4 animate-slide-up">
          <div className="card">
            <div className="flex flex-col sm:flex-row items-center gap-4 sm:gap-8">
              <ScoreRing score={submission.score || 0} />
              <div className="w-full sm:flex-1 text-center sm:text-left">
                <p className="font-semibold text-lg mb-1">Resultado de la Evaluación</p>
                <p className="text-foreground-muted text-sm leading-relaxed">{submission.feedback.overall}</p>
                <div className="flex gap-4 mt-3">
                  <span className="text-accent font-bold text-sm">+{submission.xp_earned} XP</span>
                  {submission.hints_used > 0 && <span className="text-foreground-muted text-sm">{submission.hints_used} pistas usadas</span>}
                </div>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {([
              { key: "variables", label: "Variables de decisión", icon: "🔢" },
              { key: "objective", label: "Función objetivo", icon: "🎯" },
              { key: "constraints", label: "Restricciones", icon: "🔒" },
              { key: "classification", label: "Clasificación del modelo", icon: "🏷️" },
            ] as const).map(({ key, label, icon }) => {
              const comp = submission.feedback![key];
              const pct = Math.round((comp.score / comp.max) * 100);
              return (
                <div key={key} className="card">
                  <div className="flex items-center justify-between mb-2">
                    <p className="text-sm font-medium">{icon} {label}</p>
                    <span className={clsx("text-sm font-bold", pct >= 80 ? "text-accent" : pct >= 50 ? "text-accent-warn" : "text-destructive")}>
                      {comp.score}/{comp.max}
                    </span>
                  </div>
                  <div className="h-1.5 bg-surface-2 rounded-full mb-2">
                    <div className={clsx("h-full rounded-full", pct >= 80 ? "bg-accent" : pct >= 50 ? "bg-accent-warn" : "bg-destructive")} style={{ width: `${pct}%` }} />
                  </div>
                  <p className="text-xs text-foreground-muted">{comp.comment}</p>
                </div>
              );
            })}
          </div>

          {submission.feedback.hints.length > 0 && (
            <div className="card border-primary/20 bg-primary/5">
              <p className="text-sm font-medium text-primary mb-2">💡 Sugerencias para mejorar</p>
              <ul className="space-y-1">
                {submission.feedback.hints.map((hint, i) => (
                  <li key={i} className="text-sm text-foreground-muted">• {hint}</li>
                ))}
              </ul>
            </div>
          )}

          <button onClick={() => { setSubmission(null); setContent(""); }}
            className="btn-secondary w-full">
            🔄 Intentar nuevamente
          </button>
        </div>
      )}

      {submission?.evaluation_status === "error" && (
        <div className="card border-destructive/30 bg-destructive/10">
          <p className="text-destructive text-sm">Hubo un error al evaluar. Intenta nuevamente.</p>
          <button onClick={() => setSubmission(null)} className="btn-secondary mt-3 text-sm">Reintentar</button>
        </div>
      )}
    </div>
  );
}
