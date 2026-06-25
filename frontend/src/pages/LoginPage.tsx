import { useState } from "react";
import type { ComponentProps } from "react";
import { login } from "../api/auth";
import { getProfile } from "../api/user";
import { useAuth } from "../hooks/useAuth";
import { useNavigate } from "react-router-dom";
function LoginPage() {
  const { setCurrentUser: loginUser } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

const handleSubmit: ComponentProps<"form">["onSubmit"] = async (e) => {
  e.preventDefault();

  try {
    await login(username, password);

    const user = await getProfile();

    loginUser(user);

    navigate("/dashboard");
  } catch (error) {
    console.error(error);
  }
};

  return (
    <div className="flex min-h-[80vh] items-center justify-center">
      <div className="w-full max-w-md rounded-xl border border-zinc-800 bg-zinc-900 p-8">
        <h1 className="mb-6 text-3xl font-bold text-white">Login</h1>

        <form className="space-y-4" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Username"
            className="w-full rounded-lg bg-zinc-800 p-3 text-white outline-none placeholder:text-zinc-400"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />

          <input
            type="password"
            placeholder="Password"
            className="w-full rounded-lg bg-zinc-800 p-3 text-white outline-none placeholder:text-zinc-400"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />

          <button
            type="submit"
            className="w-full rounded-lg bg-blue-600 p-3 font-medium text-white transition hover:bg-blue-700"
          >
            Login
          </button>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;