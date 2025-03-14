import { Link, useNavigate } from "react-router-dom";
import { Bell, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import { useAuthStore } from "@/store/authStore";
import { TickerSearch } from "@/components/search/TickerSearch";
import toast from "react-hot-toast";
import { NotificationPopover } from "@/components/notification/NotificationPopover";

export const Navbar = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuthStore();

  const handleLogout = () => {
    // Show a loading toast
    const loadingToast = toast.loading("Logging out...");

    try {
      // Call the enhanced logout function that will clear all caches
      logout();

      // Dismiss loading toast and show success
      toast.dismiss(loadingToast);
      toast.success("Logged out successfully");

      // Navigate back to login page
      navigate("/login");
    } catch (error) {
      console.error("Error during logout:", error);
      toast.dismiss(loadingToast);
      toast.error("Failed to log out properly");
    }
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
                  <NotificationPopover />
                </div>
                <Link to="/profile">
                  <Button variant="ghost" size="icon" className="relative">
                    <User className="h-5 w-5" />
                    <span className="absolute -bottom-4 text-xs font-medium text-gray-600 whitespace-nowrap">
                      {/* OPTIONAL: Add username below profile  */}
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
