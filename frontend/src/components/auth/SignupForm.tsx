import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuthStore } from "../../store/authStore";
import { authApi } from "../../api/auth";
import { SignupCredentials } from "../../types";

export const SignupForm = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState<SignupCredentials>({
    email: "",
    password: "",
    password_confirm: "",
  });
  const [error, setError] = useState("");
  const setToken = useAuthStore((state) => state.setToken);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // Sign up
      await authApi.signup(formData);

      // Login after successful signup
      const tokenResponse = await authApi.login({
        email: formData.email,
        password: formData.password,
      });

      setToken(tokenResponse.access_token);
      navigate("/profile");
    } catch (err: any) {
      setError(err.response?.data?.detail || "Signup failed");
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
    </form>
  );
};
