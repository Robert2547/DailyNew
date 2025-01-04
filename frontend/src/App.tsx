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
import { Toaster } from "react-hot-toast"; // Add this
import { DashboardPage } from "./pages/DashboardPage";
import { CompanyPage } from "./pages/CompanyPage";
import { Mock } from "./pages/mockup/Mock";

const queryClient = new QueryClient();

function App() {
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
              <>
                {/*<Route path="/profile" element={<ProfilePage />} /> */}
                <Route path="/dashboard" element={<DashboardPage />} />
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
                <Route path="/company/:symbol" element={<CompanyPage />} />
                <Route path="/mock" element={<Mock />} />
              </>
            </Route>
          </Route>

          {/* Redirect root to login */}
        </Routes>
      </Router>
    </QueryClientProvider>
  );
}

export default App;
