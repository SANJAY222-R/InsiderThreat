/**
 * Main Layout
 *
 * Primary application layout with sidebar navigation, header, and content area.
 *
 * Phase 0: Stub component only.
 *
 * TODO (Phase 8): Implement responsive layout with sidebar toggle.
 */

import { type ReactNode } from "react";

interface MainLayoutProps {
  children: ReactNode;
}

export function MainLayout({ children }: MainLayoutProps) {
  return (
    <div id="layout-main" className="layout-main">
      {/* TODO: Sidebar component */}
      {/* TODO: Header component */}
      <main className="layout-content">
        {children}
      </main>
    </div>
  );
}
