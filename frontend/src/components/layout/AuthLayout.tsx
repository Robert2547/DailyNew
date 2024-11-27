// (for login/signup - no navbar)
import { Outlet } from "react-router-dom";

export const AuthLayout = () => {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <div className="max-w-md w-full p-6 bg-white rounded-lg shadow-lg">
        <h1 className="text-2xl font-semibold text-center">Welcome to AuthLayout</h1>
        <Outlet />
      </div>
    </div>
  );
};
