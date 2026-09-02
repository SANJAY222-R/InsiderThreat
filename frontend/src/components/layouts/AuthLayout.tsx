/**
 * Auth Layout
 *
 * Minimal layout for authentication pages (login, register, forgot password).
 *
 * Phase 0: Stub component only.
 */

import { type ReactNode } from "react";

interface AuthLayoutProps {
  children: ReactNode;
}

export function AuthLayout({ children }: AuthLayoutProps) {
  return (
    <div id="layout-auth" className="layout-auth">
      <div className="auth-container">
        {children}
      </div>
    </div>
  );
}
