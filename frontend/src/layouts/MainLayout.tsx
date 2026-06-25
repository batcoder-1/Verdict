import Navbar from "../components/layout/Navbar";
import { Outlet } from "react-router-dom";

function MainLayout() {
  return (
    <div className="min-h-screen bg-zinc-950 text-white">
      <Navbar />
      <Outlet />
    </div>
  );
}

export default MainLayout;