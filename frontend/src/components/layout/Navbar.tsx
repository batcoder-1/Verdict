import { Link, useLocation, useNavigate } from "react-router-dom";
import { LayoutDashboard, User, LogOut } from "lucide-react";

import Logo from "../common/Logo";
import Button from "../common/Button";
import { useAuth } from "../../hooks/useAuth";

function Navbar() {
  const { isAuthenticated, user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = async () => {
    await logout();
    navigate("/login", { replace: true });
  };

  return (
    <nav className="sticky top-0 z-50 border-b border-zinc-800 bg-zinc-950/90 backdrop-blur">
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4">
        <Logo />

        {isAuthenticated ? (
          <div className="flex items-center gap-3">
            <Link to="/dashboard">
              <Button
                variant={
                  location.pathname === "/dashboard"
                    ? "primary"
                    : "outline"
                }
              >
                <LayoutDashboard size={18} />
                Dashboard
              </Button>
            </Link>

            <Link to="/profile">
              <Button
                variant={
                  location.pathname === "/profile"
                    ? "primary"
                    : "outline"
                }
              >
                <User size={18} />
                Profile
              </Button>
            </Link>

            {/* Avatar */}
            <div className="flex h-10 w-10 items-center justify-center rounded-full bg-blue-600 font-semibold text-white">
              {user?.username?.charAt(0).toUpperCase()}
            </div>

            <Button variant="outline" onClick={handleLogout}>
              <LogOut size={18} />
              Logout
            </Button>
          </div>
        ) : (
          <div className="flex items-center gap-3">
            <Link to="/login">
              <Button variant="outline">
                Login
              </Button>
            </Link>

            <Link to="/signup">
              <Button>
                Get Started
              </Button>
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
}

export default Navbar;