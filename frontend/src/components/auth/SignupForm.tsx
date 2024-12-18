import { useState, useEffect } from "react";
import { useNavigate, Link } from "react-router-dom";
import { useAuthStore } from "../../store/authStore";
import { authApi } from "../../api/auth";
import { SignupCredentials } from "../../types";
import toast from "react-hot-toast";
import { checkServiceHealth } from "../../utils/serviceHealth";

export const SignupForm = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<SignupCredentials>({
    email: "",
    password: "",
    password_confirm: "",
  });
  const [error, setError] = useState("");
  const setToken = useAuthStore((state) => state.setToken);

  useEffect(() => {
    const checkServices = async () => {
      const health = await checkServiceHealth();
      if (!health.auth || !health.user) {
        toast.error(health.message);
        setError(health.message);
      }
    };
    console.log("Checking services...");
    checkServices();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    // Check services before attempting signup
    const health = await checkServiceHealth();
    if (!health.auth || !health.user) {
      toast.error(health.message);
      setError(health.message);
      return;
    }

    // Add loading toast
    const loadingToast = toast.loading("Creating your account...");

    try {
      // Password match validation
      if (formData.password !== formData.password_confirm) {
        toast.dismiss(loadingToast);
        toast.error("Passwords do not match");
        setError("Passwords do not match");
        return;
      }

      // Sign up
      await authApi.signup(formData);

      // Login after successful signup
      const tokenResponse = await authApi.login({
        email: formData.email,
        password: formData.password,
      });

      setToken(tokenResponse.access_token);

      // Dismiss loading and show success
      toast.dismiss(loadingToast);
      toast.success("Account created successfully!");

      // Small delay before navigation for better UX
      setTimeout(() => {
        navigate("/profile");
      }, 1000);
    } catch (err: any) {
      toast.dismiss(loadingToast);
      // Handle validation errors array
      if (Array.isArray(err.response?.data?.detail)) {
        // Get unique error messages
        const uniqueErrors = [
          ...new Set(err.response.data.detail.map((error: any) => error.msg)),
        ];
        const errorMessage = uniqueErrors[0]; // Take just the first error
        toast.error(errorMessage as string);
        setError(errorMessage as string);
      } else {
        const errorMessage: string =
          typeof err.response?.data?.detail === "string"
            ? err.response.data.detail
            : "Signup failed. Please try again.";
        toast.error(errorMessage);
        setError(errorMessage);
      }
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <input
          type="email"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          placeholder="Email"
          className="w-full p-2 border rounded"
          required
        />
      </div>
      <div>
        <input
          type="password"
          value={formData.password}
          onChange={(e) =>
            setFormData({ ...formData, password: e.target.value })
          }
          placeholder="Password"
          className="w-full p-2 border rounded"
          required
        />
      </div>
      <div>
        <input
          type="password"
          value={formData.password_confirm}
          onChange={(e) =>
            setFormData({ ...formData, password_confirm: e.target.value })
          }
          placeholder="Confirm Password"
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
        Sign Up
      </button>

      <div className="text-center">
        <span className="text-gray-600">Already have an account? </span>
        <Link
          to="/login"
          className="text-blue-500 hover:text-blue-700 font-medium"
        >
          Login
        </Link>
      </div>
    </form>
  );
};
