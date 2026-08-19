import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// Redirect logged-in users away from these (no point visiting login/register if already in)
const AUTH_ONLY_PUBLIC = ["/login", "/register"];
// Always accessible regardless of session (email links land here)
const ALWAYS_PUBLIC = ["/verify-email", "/forgot-password", "/reset-password"];

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;
  // Session is alive if EITHER token is present. The access token is short-lived
  // (1h); the refresh token lasts 30 days and the API client silently refreshes
  // the access token on demand. Checking only the access token would bounce the
  // user to /login on every navigation once it expires — even mid-session.
  const token =
    request.cookies.get("access_token")?.value ||
    request.cookies.get("refresh_token")?.value;

  if (ALWAYS_PUBLIC.some((p) => pathname.startsWith(p))) {
    return NextResponse.next();
  }
  if (AUTH_ONLY_PUBLIC.some((p) => pathname.startsWith(p))) {
    if (token) return NextResponse.redirect(new URL("/dashboard", request.url));
    return NextResponse.next();
  }
  if (!token) {
    return NextResponse.redirect(new URL("/login", request.url));
  }
  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!_next/static|_next/image|favicon.ico|api).*)"],
};
