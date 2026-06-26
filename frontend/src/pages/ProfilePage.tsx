import { Link } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

import ProfileForm from "../components/profile/ProfileForm";

const ProfilePage = () => {
  return (
    <div className="mx-auto max-w-3xl space-y-8">
      <Link
        to="/dashboard"
        className="inline-flex items-center gap-2 text-zinc-400 transition hover:text-white"
      >
        <ArrowLeft size={18} />
        Back to Dashboard
      </Link>

      <div>
        <h1 className="text-4xl font-bold">
          Account Settings
        </h1>

        <p className="mt-2 text-zinc-400">
          Manage your competitive programming profiles.
        </p>
      </div>

      <ProfileForm />
    </div>
  );
};

export default ProfilePage;