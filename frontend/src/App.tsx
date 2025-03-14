import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { LoginForm } from "./pages/LoginForm";
import { PrivateRoute } from "./components/auth/PrivateRoute";
import { MainLayout } from "./components/layout/MainLayout";
import { AuthLayout } from "./components/layout/AuthLayout";
import { SignupForm } from "./pages/SignupForm";
import { Toaster } from "react-hot-toast";
import { DashboardPage } from "./pages/DashboardPage";
import { CompanyPage } from "./pages/CompanyPage";
import APIErrorPage from "./pages/APIError";
import { Mock } from "./pages/mockup/Mock";
import { ProfilePage } from "./pages/ProfilePage";
import { WatchlistPage } from "./pages/WatchlistPage";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: (failureCount, error: any) => {
        // Don't retry on rate limit errors
        if (error?.message?.includes("rate limit")) {
          return false;
        }
        return failureCount < 3;
      },
      // Add staleTime to reduce unnecessary refetches
      staleTime: 5 * 60 * 1000, // 5 minutes
      // Add gcTime to keep data in cache longer
      gcTime: 30 * 60 * 1000, // 30 minutes
    },
  },
});

function App() {
  // No prefetching implementation

  return (
    <QueryClientProvider client={queryClient}>
      <Toaster
        position="top-center"
        toastOptions={{
          success: {
            duration: 3000,
            style: {
              background: "#10B981",
              color: "white",
            },
          },
          error: {
            duration: 4000,
            style: {
              background: "#EF4444",
              color: "white",
            },
          },
          loading: {
            style: {
              background: "#3B82F6",
              color: "white",
            },
          },
        }}
      />
      <Router>
        <Routes>
          {/* Auth routes (no navbar) */}
          <Route element={<AuthLayout />}>
            <Route path="/login" element={<LoginForm />} />
            <Route path="/signup" element={<SignupForm />} />
          </Route>

          {/* Protected routes (with navbar) */}
          <Route element={<PrivateRoute />}>
            <Route element={<MainLayout />}>
              <Route path="/dashboard" element={<DashboardPage />} />
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="/company/:symbol" element={<CompanyPage />} />
              <Route path="/mock" element={<Mock />} />
              <Route path="/profile" element={<ProfilePage />} />
              <Route path="/watchlist" element={<WatchlistPage />} />
            </Route>
          </Route>

          {/* Error routes (accessible from anywhere) */}
          <Route path="/error" element={<APIErrorPage />} />
        </Routes>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
