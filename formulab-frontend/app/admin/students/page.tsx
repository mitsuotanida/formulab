"use client";
import { useEffect, useState } from "react";
import Link from "next/link";
import api from "@/lib/api";
import { LEVEL_NAMES } from "@/lib/types";

interface Student { id: string; name: string; email: string; xp: number; level: number; streak: number; }

export default function AdminStudentsPage() {
  const [students, setStudents] = useState<Student[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.get("/users?per_page=100").then((r) => setStudents(r.data)).finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-6 animate-fade-in">
      <div>
        <h1 className="text-2xl font-bold">👥 Estudiantes</h1>
        <p className="text-foreground-muted text-sm mt-1">{students.length} estudiantes registrados</p>
      </div>
      <div className="card p-0 overflow-hidden">
        <table className="w-full text-sm">
          <thead>
            <tr className="border-b border-border">
              {["Nombre", "Email", "Nivel", "XP", "Racha", "Perfil"].map((h) => (
                <th key={h} className="text-left px-6 py-4 text-foreground-muted font-medium text-xs uppercase tracking-wider">{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {loading ? (
              [...Array(5)].map((_, i) => (
                <tr key={i} className="border-b border-border">
                  {[...Array(6)].map((_, j) => <td key={j} className="px-6 py-4"><div className="h-4 bg-surface-2 rounded animate-pulse" /></td>)}
                </tr>
              ))
            ) : students.map((s) => (
              <tr key={s.id} className="border-b border-border last:border-0 hover:bg-surface-2 transition-colors">
                <td className="px-6 py-4 font-medium">{s.name}</td>
                <td className="px-6 py-4 text-foreground-muted">{s.email}</td>
                <td className="px-6 py-4"><span className="text-primary text-xs font-medium">{LEVEL_NAMES[s.level]}</span></td>
                <td className="px-6 py-4 font-mono text-accent">{s.xp.toLocaleString()}</td>
                <td className="px-6 py-4 text-accent-warn">🔥 {s.streak}</td>
                <td className="px-6 py-4">
                  <Link href={`/admin/students/${s.id}`} className="text-primary text-xs hover:text-primary-light transition-colors">Ver detalle →</Link>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
