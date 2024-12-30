
import { Link } from 'react-router-dom';
import { Bell, Search, User } from 'lucide-react';
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useAuthStore } from '../../store/authStore';

export const Navbar = () => {
  const { user, logout } = useAuthStore();

  return (
    <nav className="bg-white border-b border-gray-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex-shrink-0 flex items-center">
            <Link to="/" className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-blue-400 bg-clip-text text-transparent">
              DailyNews
            </Link>
          </div>

          {/* Search */}
          <div className="hidden sm:flex-1 sm:flex sm:items-center sm:justify-center max-w-2xl">
            <div className="relative w-full">
              <Input
                type="text"
                placeholder="Search companies..."
                className="w-full pl-10"
              />
              <Search className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
            </div>
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
                  <Button variant="ghost" size="icon">
                    <User className="h-5 w-5" />
                  </Button>
                </Link>
                <Button
                  onClick={logout}
                  variant="outline"
                  className="text-red-600"
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