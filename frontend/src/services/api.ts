/**
 * API Service
 *
 * Base API client with authentication header injection.
 *
 * Phase 0: Stub only.
 *
 * TODO (Phase 8): Implement with fetch/axios and interceptors.
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";

export const api = {
  baseUrl: API_BASE_URL,

  async get<T>(_endpoint: string): Promise<T> {
    throw new Error("Not implemented");
  },

  async post<T>(_endpoint: string, _data: unknown): Promise<T> {
    throw new Error("Not implemented");
  },

  async put<T>(_endpoint: string, _data: unknown): Promise<T> {
    throw new Error("Not implemented");
  },

  async delete(_endpoint: string): Promise<void> {
    throw new Error("Not implemented");
  },
};
