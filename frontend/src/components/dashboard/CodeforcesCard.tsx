import { useEffect, useState } from "react";
import {
  getCodeforcesProfile,
  syncCodeforcesProfile,
} from "../../api/codeforces";
import type { CodeforcesProfile } from "../../types/codeforces";
import SectionCard from "../common/SectionCard";
import Button from "../common/Button";
import StatCard from "../common/StatCard";
import {
  Trophy,
  Flame,
  TrendingUp,
  Medal,
  Users,
  Globe,
  Award,
  Crown,
} from "lucide-react";
import { toast } from "sonner";
const CodeforcesCard = () => {
  const [profile, setProfile] = useState<CodeforcesProfile | null>(null);
  const [loading, setLoading] = useState(true);
  const [syncing, setSyncing] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchProfile = async () => {
      try {
        const data = await getCodeforcesProfile();
        setProfile(data);
      } catch {
        setError("Failed to load Codeforces profile");
      } finally {
        setLoading(false);
      }
    };

    fetchProfile();
  }, []);

  const handleSync = async () => {
  try {
    setSyncing(true);

    const data = await syncCodeforcesProfile();
    setProfile(data);

    toast.success("Codeforces profile synced successfully!");
  } catch {
    setError("Failed to sync Codeforces profile");
    toast.error("Failed to sync Codeforces profile.");
  } finally {
    setSyncing(false);
  }
};

  if (loading) {
    return (
      <SectionCard title="Codeforces">
        Loading...
      </SectionCard>
    );
  }

  if (error) {
    return (
      <SectionCard title="Codeforces">
        <p className="text-red-500">{error}</p>
      </SectionCard>
    );
  }

  return (
  <SectionCard
    title="Codeforces"
    action={
      <Button onClick={handleSync} disabled={syncing}>
        {syncing ? "Syncing..." : "Sync"}
      </Button>
    }
  >
    <div className="grid grid-cols-2 gap-4">
      <StatCard
        title="Rating"
        value={profile?.rating ?? "N/A"}
        icon={<TrendingUp size={18} />}
      />

      <StatCard
        title="Max Rating"
        value={profile?.max_rating ?? "N/A"}
        icon={<Trophy size={18} />}
      />

      <StatCard
        title="Rank"
        value={profile?.rank ?? "N/A"}
        icon={<Award size={18} />}
      />

      <StatCard
        title="Max Rank"
        value={profile?.max_rank ?? "N/A"}
        icon={<Crown size={18} />}
      />

      <StatCard
        title="Current Streak"
        value={profile?.current_streak ?? 0}
        icon={<Flame size={18} />}
      />

      <StatCard
        title="Current Year Best Streak"
        value={profile?.current_year_longest_streak ?? 0}
        icon={<Medal size={18} />}
      />

      <StatCard
        title="Country"
        value={profile?.country ?? "N/A"}
        icon={<Globe size={18} />}
      />

      <StatCard
        title="Friends"
        value={profile?.friendsCount ?? 0}
        icon={<Users size={18} />}
      />
    </div>

    <p className="mt-6 text-right text-xs text-zinc-500">
      Last Synced: {profile?.last_synced ?? "Never"}
    </p>
  </SectionCard>
);
};

export default CodeforcesCard;