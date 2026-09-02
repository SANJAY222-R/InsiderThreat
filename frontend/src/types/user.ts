/**
 * User Type Definitions
 */

export interface User {
  id: number;
  username: string;
  email: string;
  role: "admin" | "analyst" | "auditor" | "viewer";
  isActive: boolean;
}

export interface UserCreate {
  username: string;
  email: string;
  password: string;
  role: string;
}

export interface UserLogin {
  username: string;
  password: string;
}
