export interface Exercise {
  id: string;
  title: string;
  description: string;
  data_table?: { headers: string[]; rows: string[][] } | null;
  domain: string;
  type: "LP" | "MIP" | "NLP";
  difficulty: "easy" | "medium" | "hard";
  ra_ids: number[];
  ai_generated: boolean;
  hints_count: number;
  hints?: Array<{ order: number; text: string }>;
  created_at: string;
  user_best_score?: number | null;
  user_attempts: number;
}

export interface FeedbackComponent {
  score: number;
  max: number;
  comment: string;
}

export interface SubmissionFeedback {
  overall: string;
  variables: FeedbackComponent;
  objective: FeedbackComponent;
  constraints: FeedbackComponent;
  classification: FeedbackComponent;
  hints: string[];
}

export interface Submission {
  id: string;
  exercise_id: string;
  score?: number;
  xp_earned: number;
  hints_used: number;
  evaluation_status: "pending" | "evaluating" | "complete" | "error";
  feedback?: SubmissionFeedback;
  badges_earned: Array<{ id: number; name: string; icon: string }>;
  level_up?: string;
  created_at: string;
}

export interface Badge {
  id: number;
  name: string;
  description: string;
  icon: string;
  condition_type: string;
  condition_value: Record<string, unknown>;
  xp_reward: number;
  earned: boolean;
  earned_at?: string;
}

export interface RATracking {
  ra_id: number;
  label: string;
  attempts: number;
  successes: number;
  success_rate: number;
  last_attempt?: string;
}

export interface LeaderboardEntry {
  rank: number;
  user_id: string;
  name: string;
  xp: number;
  level: number;
  level_name: string;
  streak: number;
  exercises_completed: number;
}

export const LEVEL_NAMES: Record<number, string> = {
  1: "Intern", 2: "Junior", 3: "Engineer", 4: "Senior", 5: "Staff", 6: "Principal",
};

export const DIFFICULTY_LABELS: Record<string, string> = {
  easy: "Fácil", medium: "Medio", hard: "Difícil",
};

export const TYPE_LABELS: Record<string, string> = {
  LP: "Prog. Lineal", MIP: "Prog. Entera Mixta", NLP: "Prog. No Lineal",
};

export const DOMAIN_LABELS: Record<string, string> = {
  production: "Producción", logistics: "Logística", agriculture: "Agricultura",
  finance: "Finanzas", inventory: "Inventario", energy: "Energía", generic: "General",
};
