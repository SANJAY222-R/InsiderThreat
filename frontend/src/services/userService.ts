import { api } from "./api";
import type { User, UserUpdate } from "../types/user";

export const userService = {
  async getUsers(params?: { skip?: number; limit?: number }): Promise<User[]> {
    return api.get<User[]>("/users/", { params });
  },

  async getUser(userId: string): Promise<User> {
    return api.get<User>(`/users/${userId}`);
  },

  async updateUser(userId: string, data: UserUpdate): Promise<User> {
    return api.put<User>(`/users/${userId}`, data);
  },

  async deactivateUser(userId: string): Promise<User> {
    return api.delete<User>(`/users/${userId}`);
  },
};
