import axios from "axios";
import { Profile } from "../types";

const USER_API_URL = "http://localhost:8002/api/v1/profiles";

/**
 * Profile API service
 */
export const profileApi = {
  /**
   * Get logged-in user's profile
   */
  getMyProfile: async (token: string): Promise<Profile> => {
    const response = await axios.get(`${USER_API_URL}/me`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return response.data;
  },

  /**
   * Get all profiles (paginated)
   */
  getProfiles: async (
    token: string,
    skip = 0,
    limit = 100
  ): Promise<Profile[]> => {
    const response = await axios.get(
      `${USER_API_URL}/?skip=${skip}&limit=${limit}`,
      {
        headers: { Authorization: `Bearer ${token}` },
      }
    );
    return response.data;
  },
};
