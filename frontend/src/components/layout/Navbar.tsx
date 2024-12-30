// src/components/layout/Navbar.tsx
import { Link, useNavigate } from "react-router-dom";
import { Bell, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAuthStore } from "@/store/authStore";
import { TickerSearch } from "@/components/search/TickerSearch";
import toast from "react-hot-toast";

export const Navbar = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();

  const handleLogout = () => {
    logout();
    toast.success("Logged out successfully");
    navigate("/login");
  };

  return (
    <nav className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex-shrink-0 flex items-center">
            <Link
              to="/"
              className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-blue-400 bg-clip-text text-transparent"
            >
              DailyNews
            </Link>
          </div>

          {/* Search */}
          <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-center max-w-2xl">
            <TickerSearch />
          </div>

          {/* Right Nav Items */}
          <div className="flex items-center space-x-4">
            {user ? (
              <>
                <div className="relative">
                  <Button variant="ghost" size="icon">
                    <Bell className="h-5 w-5" />
                  </Button>
                  <span className="absolute top-0 right-0 w-2 h-2 rounded-full bg-red-500"></span>
                </div>
                <Link to="/profile">
                  <Button variant="ghost" size="icon" className="relative">
                    <User className="h-5 w-5" />
                    <span className="absolute -bottom-4 text-xs font-medium text-gray-600 whitespace-nowrap">
                      {user.email.split("@")[0]}
                    </span>
                  </Button>
                </Link>
                <Button
                  onClick={handleLogout}
                  variant="outline"
                  className="text-red-600 hover:text-red-700 hover:bg-red-50"
                >
                  Logout
                </Button>
              </>
            ) : (
              <>
                <Link to="/login">
                  <Button variant="ghost">Login</Button>
                </Link>
                <Link to="/signup">
                  <Button variant="default">Sign Up</Button>
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};
