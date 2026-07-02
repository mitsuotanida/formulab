import Cookies from "js-cookie";

export interface User {
  id: string;
  name: string;
  nickname?: string;
  email: string;
  role: "student" | "teacher";
  xp: number;
  level: number;
  streak: number;
}

export function getStoredUser(): User | null {
  if (typeof window === "undefined") return null;
  const raw = localStorage.getItem("formulab_user");
  return raw ? JSON.parse(raw) : null;
}

export function storeSession(accessToken: string, refreshToken: string, user: User) {
  Cookies.set("access_token", accessToken, { expires: 1 / 24, sameSite: "lax" });
  Cookies.set("refresh_token", refreshToken, { expires: 30, sameSite: "lax" });
  localStorage.setItem("formulab_user", JSON.stringify(user));
}

export function clearSession() {
  Cookies.remove("access_token");
  Cookies.remove("refresh_token");
  localStorage.removeItem("formulab_user");
}

export function isLoggedIn(): boolean {
  return !!Cookies.get("access_token");
}
