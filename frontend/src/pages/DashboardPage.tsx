import { useEffect, useState } from "react";
import { useAuth } from "../hooks/useAuth";

import ProfileSummary from "../components/dashboard/ProfileSummary";
import LeetCodeCard from "../components/dashboard/LeetcodeCard";
import CodeforcesCard from "../components/dashboard/CodeforcesCard";
import ContestHistory from "../components/dashboard/ContestHistory";
import LeetCodeRatingChart from "../components/dashboard/LeetcodeRatingChart";
import CodeforcesRatingChart from "../components/dashboard/CodeforcesRatingChart";

import {
  getLeetCodeContests,
  getCodeforcesContests,
} from "../api/contest";

import type { LeetCodeContest } from "../types/leetcode";
import type { CodeforcesContest } from "../types/codeforces";

const DashboardPage = () => {
  const { user } = useAuth();

  const [leetcodeContests, setLeetcodeContests] = useState<LeetCodeContest[]>([]);
  const [codeforcesContests, setCodeforcesContests] = useState<CodeforcesContest[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchContests = async () => {
      try {
        const [lc, cf] = await Promise.all([
          getLeetCodeContests(),
          getCodeforcesContests(),
        ]);

        setLeetcodeContests(lc);
        setCodeforcesContests(cf);
      } finally {
        setLoading(false);
      }
    };

    fetchContests();
  }, []);

  return (
    <div className="space-y-8">
     <div className="mb-8">
  <h1 className="text-4xl font-bold">
    Welcome back, {user?.username} 👋
  </h1>

  <p className="mt-2 text-lg text-zinc-400">
    Track your competitive programming journey.
  </p>
</div>
      <ProfileSummary />

      <div className="grid gap-6 lg:grid-cols-2">
        <LeetCodeCard />
        <CodeforcesCard />
      </div>

     <div className="grid gap-6 lg:grid-cols-2">
    <LeetCodeRatingChart contests={leetcodeContests} />

    <CodeforcesRatingChart contests={codeforcesContests} />
     </div>

      <ContestHistory
        loading={loading}
        leetcode={leetcodeContests}
        codeforces={codeforcesContests}
        setLeetcode={setLeetcodeContests}
        setCodeforces={setCodeforcesContests}
      />
    </div>
  );
};

export default DashboardPage;