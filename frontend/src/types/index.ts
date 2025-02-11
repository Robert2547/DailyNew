/**
 * User interface
 */
export interface User {
  id: number;
  email: string;
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

export interface CompanySearchResult {
  symbol: string;
  name: string;
  type: string;
  region: string;
}

export interface CompanyOverview {
  Symbol: string;
  Name: string;
  Description: string;
  Exchange: string;
  Currency: string;
  Country: string;
  Sector: string;
  Industry: string;
  MarketCapitalization: string;
}
