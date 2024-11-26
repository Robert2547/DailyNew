import axios from "axios";
import {
  SignupCredentials,
  LoginCredentials,
  TokenResponse,
  User,
} from "../types";

const AUTH_API_URL = "http://localhost:8001/api/v1/auth";

/**
 * Authentication API service
 */
export const authApi = {
  /**
   * User signup
   */
  signup: async (credentials: SignupCredentials): Promise<User> => {
    const response = await axios.post(`${AUTH_API_URL}/signup`, credentials);
    return response.data;
  },

  /**
   * User login
   */
  login: async (credentials: LoginCredentials): Promise<TokenResponse> => {
    const response = await axios.post(`${AUTH_API_URL}/login`, credentials);
    return response.data;
  },

  /**
   * Verify token
   */
  verifyToken: async (token: string): Promise<User> => {
    const response = await axios.post(
      `${AUTH_API_URL}/verify-token`,
      {},
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    return response.data;
  },
};
