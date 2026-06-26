import { Link } from "react-router-dom";
import { useAuth } from "../../hooks/useAuth";
import SectionCard from "../common/SectionCard";
import Button from "../common/Button";
import StatCard from "../common/StatCard";

const ProfileSummary = () => {
  const { user } = useAuth();

  return (
    <SectionCard title="Profile">
      <div className="grid gap-4 md:grid-cols-3">
        <StatCard
          title="Username"
          value={user?.username ?? "N/A"}
        />

        <StatCard
          title="LeetCode"
          value={user?.leetcode_handle ?? "Not Linked"}
        />

        <StatCard
          title="Codeforces"
          value={user?.codeforces_handle ?? "Not Linked"}
        />
      </div>

      <div className="mt-6 flex justify-end">
        <Link to="/profile">
          <Button>Edit Profile</Button>
        </Link>
      </div>
    </SectionCard>
  );
};

export default ProfileSummary;