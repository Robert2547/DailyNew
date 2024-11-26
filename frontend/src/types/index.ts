/**
 * User interface
 */
export interface User {
  id: number;
  email: string;
  is_active: boolean;
}

/**
 * Profile interface
 */
export interface Profile {
  id: number;
  auth_user_id: number;
  email: string;
}

/**
 * Login request payload
 */
export interface LoginCredentials {
  email: string;
  password: string;
}

/**
 * Registration request payload
 */
export interface SignupCredentials {
  email: string;
  password: string;
  password_confirm: string;
}

/**
 * Token response from login
 */
export interface TokenResponse {
  access_token: string;
  token_type: string;
}
