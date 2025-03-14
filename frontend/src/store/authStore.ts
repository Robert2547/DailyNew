// authStore.ts with improved logout
import { create } from "zustand";
import { persist, createJSONStorage } from "zustand/middleware";
import { User } from "../types";

// Import the store clear functions
import { clearWatchlistCache } from "./watchlistStore";
import { clearAlphavantageCache } from "../services/alphavantage";

interface AuthState {
  user: User | null;
  token: string | null;
  setUser: (user: User) => void;
  setToken: (token: string) => void;
  setAuth: (user: User, token: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      setUser: (user) => set({ user }),
      setToken: (token) => set({ token }),
      setAuth: (user, token) => set({ user, token }),
      logout: () => {
        // Clear all user-specific data from stores
        clearWatchlistCache();
        clearAlphavantageCache();

        // Then clear the auth state
        set({ user: null, token: null });
      },
    }),
    {
      name: "auth-storage",
      storage: createJSONStorage(() => localStorage),
    }
  )
);

// Helper to check if user is authenticated
export const isAuthenticated = () => {
  const { token, user } = useAuthStore.getState();
  return !!(token && user);
};
