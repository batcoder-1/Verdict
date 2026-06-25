import { createContext, useEffect, useState } from "react";
import type { ReactNode } from "react";
import type { User } from "../types/user";
import { getProfile } from "../api/user";
import { logout as logoutApi } from "../api/auth";

interface AuthContextType {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;

  setCurrentUser: (user: User) => void;
  logout: () => Promise<void>;
}

export const AuthContext = createContext<AuthContextType | undefined>(
  undefined
);

interface AuthProviderProps {
  children: ReactNode;
}

export function AuthProvider({ children }: AuthProviderProps) {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  const isAuthenticated = user !== null;

  const setCurrentUser = (user: User) => {
    setUser(user);
  };

  const logout = async () => {
    try {
      await logoutApi();
    } finally {
      setUser(null);
    }
  };

  useEffect(() => {
    async function restoreSession() {
      try {
        const user = await getProfile();
        setUser(user);
      } catch {
        // User is not logged in
      } finally {
        setLoading(false);
      }
    }

    restoreSession();
  }, []);

  if (loading) {
    return <div>Loading...</div>;
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        isAuthenticated,
        loading,
        setCurrentUser,
        logout,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}