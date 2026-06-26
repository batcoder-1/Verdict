import { useAuth } from "../hooks/useAuth";
import ProfileSummary from "../components/dashboard/ProfileSummary";
import LeetCodeCard from "../components/dashboard/LeetcodeCard";
import CodeforcesCard from "../components/dashboard/CodeforcesCard";
import ContestHistory from "../components/dashboard/ContestHistory";

const DashboardPage = () => {
  const { user } = useAuth();

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">
        Welcome back, {user?.username}! 👋
      </h1>

      <ProfileSummary />

      <div className="grid gap-6 md:grid-cols-2">
        <LeetCodeCard />
        <CodeforcesCard />
      </div>

      <ContestHistory />
    </div>
  );
};

export default DashboardPage;