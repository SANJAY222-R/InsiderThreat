import { api } from "./api";
import type { AuthToken, User, UserCreate } from "../types/user";

export const authService = {
  async login(username: string, password: string): Promise<AuthToken> {
    const formData = new FormData();
    formData.append("username", username);
    formData.append("password", password);

    const token = await api.post<AuthToken>("/auth/login", formData);
    localStorage.setItem("token", token.access_token);
    return token;
  },

  async register(data: UserCreate): Promise<User> {
    return api.post<User>("/auth/register", data);
  },

  async getMe(): Promise<User> {
    return api.get<User>("/auth/me");
  },

  logout(): void {
    localStorage.removeItem("token");
  },

  getToken(): string | null {
    return localStorage.getItem("token");
  },

  isAuthenticated(): boolean {
    return !!localStorage.getItem("token");
  },
};
