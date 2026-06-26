import { useEffect, useState } from "react";
import {
  getCodeforcesProfile,
  syncCodeforcesProfile,
} from "../../api/codeforces";
import type { CodeforcesProfile } from "../../types/codeforces";

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
    } catch {
      setError("Failed to sync Codeforces profile");
    } finally {
      setSyncing(false);
    }
  };

  if (loading) {
    return (
      <div className="rounded-xl border p-6">
        Loading...
      </div>
    );
  }

  if (error) {
    return (
      <div className="rounded-xl border p-6 text-red-500">
        {error}
      </div>
    );
  }

  return (
    <div className="rounded-xl border p-6 space-y-3">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">Codeforces</h2>

        <button
          onClick={handleSync}
          disabled={syncing}
          className="rounded bg-green-600 px-3 py-2 text-white hover:bg-green-700 disabled:opacity-50"
        >
          {syncing ? "Syncing..." : "Sync"}
        </button>
      </div>

      <p>Rating: {profile?.rating ?? "N/A"}</p>
      <p>Max Rating: {profile?.max_rating ?? "N/A"}</p>
      <p>Rank: {profile?.rank ?? "N/A"}</p>
      <p>Max Rank: {profile?.max_rank ?? "N/A"}</p>
      <p>Country: {profile?.country ?? "N/A"}</p>
      <p>Friends: {profile?.friendsCount ?? "N/A"}</p>

      <hr />

      <p>Current Streak: {profile?.current_streak ?? "N/A"}</p>
      <p>Best Streak: {profile?.current_year_longest_streak ?? "N/A"}</p>

      <p className="text-sm text-gray-500">
        Last Synced: {profile?.last_synced ?? "Never"}
      </p>
    </div>
  );
};

export default CodeforcesCard;