import { Link } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";

const ProfileSummary = () => {
  const { user } = useAuth();

  return (
    <div className="rounded-xl border p-6">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">Profile</h2>

        <Link
          to="/profile"
          className="rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700"
        >
          Edit Profile
        </Link>
      </div>

      <div className="mt-4 space-y-2">
        <p><strong>Username:</strong> {user?.username}</p>
        <p><strong>LeetCode:</strong> {user?.leetcode_handle || "Not Linked"}</p>
        <p><strong>Codeforces:</strong> {user?.codeforces_handle || "Not Linked"}</p>
      </div>
    </div>
  );
};

export default ProfileSummary;