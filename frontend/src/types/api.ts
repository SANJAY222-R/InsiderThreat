/**
 * API Type Definitions
 *
 * Shared types for API request/response structures.
 */

export interface ApiResponse<T> {
  success: boolean;
  data: T | null;
  message: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

export interface ApiError {
  success: false;
  errorCode: string;
  message: string;
  details: Record<string, unknown>;
}
