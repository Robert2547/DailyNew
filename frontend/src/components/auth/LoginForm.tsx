import { useState } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuthStore } from "../../store/authStore";
import { authApi } from "../../api/auth";
import { LoginCredentials } from "../../types";
import toast from "react-hot-toast";

export const LoginForm = () => {
  const navigate = useNavigate();
  const [credentials, setCredentials] = useState<LoginCredentials>({
    email: "",
    password: "",
  });
  const [error, setError] = useState("");
  const setToken = useAuthStore((state) => state.setToken);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    const loadingToast = toast.loading("Logging in...");

    try {
      const response = await authApi.login(credentials);
      setToken(response.access_token);

      // Dismiss loading and show success
      toast.dismiss(loadingToast);
      toast.success("Successfully logged in!");

      // Small delay before navigation
      setTimeout(() => {
        navigate("/profile");
      }, 1000);
    } catch (err: any) {
      // Dismiss loading and show error
      toast.dismiss(loadingToast);
      const errorMessage = err.response?.data?.detail || "Login failed";
      toast.error(errorMessage);
      setError(errorMessage);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <input
          type="email"
          value={credentials.email}
          onChange={(e) =>
            setCredentials({ ...credentials, email: e.target.value })
          }
          placeholder="Email"
          className="w-full p-2 border rounded"
          required
        />
      </div>
      <div>
        <input
          type="password"
          value={credentials.password}
          onChange={(e) =>
            setCredentials({ ...credentials, password: e.target.value })
          }
          placeholder="Password"
          className="w-full p-2 border rounded"
          required
        />
      </div>
      {error && (
        <div className="text-red-500" role="alert">
          {error}
        </div>
      )}
      <button
        type="submit"
        className="w-full p-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        Login
      </button>

      <div className="text-center">
        <span className="text-gray-600">Don't have an account? </span>
        <Link
          to="/signup"
          className="text-blue-500 hover:text-blue-700 font-medium"
        >
          Sign Up
        </Link>
      </div>
    </form>
  );
};
