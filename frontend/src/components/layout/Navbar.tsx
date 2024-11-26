import { Link } from 'react-router-dom';
import { useAuthStore } from '../../store/authStore';

export const Navbar = () => {
  const { user, logout } = useAuthStore();

  return (
    <nav className="bg-white shadow">
      <div className="container mx-auto px-4">
        <div className="flex justify-between h-16">
          <div className="flex">
            <Link to="/" className="flex items-center">
              Home
            </Link>
          </div>
          
          <div className="flex items-center">
            {user ? (
              <>
                <Link to="/profile" className="px-3 py-2">
                  Profile
                </Link>
                <button
                  onClick={logout}
                  className="px-3 py-2 text-red-600"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="px-3 py-2">
                  Login
                </Link>
                <Link to="/signup" className="px-3 py-2">
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};