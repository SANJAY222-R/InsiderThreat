/**
 * Utility Functions
 *
 * Shared utility functions for the frontend.
 *
 * Phase 0: Stub only.
 */

/**
 * Concatenate class names, filtering out falsy values.
 */
export function cn(...classes: (string | undefined | null | false)[]): string {
  return classes.filter(Boolean).join(" ");
}

/**
 * Format a date string to a human-readable format.
 */
export function formatDate(dateString: string): string {
  return new Date(dateString).toLocaleDateString("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

/**
 * Format a risk score as a percentage string.
 */
export function formatRiskScore(score: number): string {
  return `${(score * 100).toFixed(1)}%`;
}
