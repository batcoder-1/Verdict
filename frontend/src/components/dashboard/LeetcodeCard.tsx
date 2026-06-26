import { useEffect, useState } from "react";
import {
  getLeetCodeProfile,
  syncLeetCodeProfile,
} from "../../api/leetcode";
import type { LeetCodeProfile } from "../../types/leetcode";
import SectionCard from "../common/SectionCard";
import Button from "../common/Button";
import StatCard from "../common/StatCard";
import {
  Trophy,
  Flame,
  Target,
  Medal,
  Hash,
  BarChart3,
  TrendingUp,
  Calendar,
} from "lucide-react";
import { toast } from "sonner";
const LeetCodeCard = () => {
  const [profile, setProfile] = useState<LeetCodeProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const data = await getLeetCodeProfile();
        setProfile(data);
      } catch {
        setError("Failed to load LeetCode profile");
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  const handleSync = async () => {
  try {
    setSyncing(true);

    const data = await syncLeetCodeProfile();
    setProfile(data);

    toast.success("LeetCode profile synced successfully!");
  } catch {
    setError("Failed to sync profile");
    toast.error("Failed to sync LeetCode profile.");
  } finally {
    setSyncing(false);
  }
};

  if (loading) {
    return (
      <SectionCard title="LeetCode">
        Loading...
      </SectionCard>
    );
  }

  if (error) {
    return (
      <SectionCard title="LeetCode">
        <p className="text-red-500">{error}</p>
      </SectionCard>
    );
  }

 return (
  <SectionCard
    title="LeetCode"
    action={
      <Button onClick={handleSync} disabled={syncing}>
        {syncing ? "Syncing..." : "Sync"}
      </Button>
    }
  >
    <div className="grid grid-cols-2 gap-4">
      <StatCard
        title="Solved"
        value={profile?.solved_problems ?? 0}
        icon={<Target size={18} />}
      />

      <StatCard
        title="Contest Rating"
        value={profile?.contest_rating ?? "N/A"}
        icon={<TrendingUp size={18} />}
      />

      <StatCard
        title="Current Streak"
        value={profile?.current_streak ?? 0}
        icon={<Flame size={18} />}
      />
      <StatCard
        title="Current Year Best Streak"
        value={profile?.max_streak_current_year ?? 0}
        icon={<Medal size={18} />}
      />
      <StatCard
        title="Contest Count"
        value={profile?.contest_count ?? 0}
        icon={<Calendar size={18} />}
      />

      <StatCard
        title="Easy"
        value={profile?.easy_solved_problems ?? 0}
        icon={<Medal size={18} />}
      />

      <StatCard
        title="Medium"
        value={profile?.medium_solved_problems ?? 0}
        icon={<BarChart3 size={18} />}
      />

      <StatCard
        title="Hard"
        value={profile?.hard_solved_problems ?? 0}
        icon={<Trophy size={18} />}
      />

      <StatCard
        title="Contest Rank"
        value={profile?.contest_ranking ?? "N/A"}
        icon={<Hash size={18} />}
      />
    </div>

    <p className="mt-6 text-right text-xs text-zinc-500">
      Last Synced: {profile?.last_synced ?? "Never"}
    </p>
  </SectionCard>
);
};

export default LeetCodeCard;