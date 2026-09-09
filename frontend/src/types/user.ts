export interface User {
  id: string;
  username: string;
  email?: string | null;
  full_name?: string | null;
  role: "admin" | "analyst" | "auditor" | "viewer" | string;
  department?: string | null;
  is_active: boolean;
  created_at?: string;
  last_login?: string | null;
}

export interface UserCreate {
  username: string;
  password: string;
  email?: string;
  full_name?: string;
  role?: string;
  department?: string;
}

export interface UserUpdate {
  email?: string;
  full_name?: string;
  role?: string;
  department?: string;
  is_active?: boolean;
}

export interface UserLogin {
  username: string;
  password: string;
}

export interface AuthToken {
  access_token: string;
  token_type: string;
  refresh_token?: string;
}
