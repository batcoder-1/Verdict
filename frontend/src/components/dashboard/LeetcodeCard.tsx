import { useEffect, useState } from "react";
import {
  getLeetCodeProfile,
  syncLeetCodeProfile,
} from "../../api/leetcode";
import type { LeetCodeProfile } from "../../types/leetcode";

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
    } catch {
      setError("Failed to sync profile");
    } finally {
      setSyncing(false);
    }
  };

  if (loading)
    return (
      <div className="rounded-xl border p-6">
        Loading...
      </div>
    );

  if (error)
    return (
      <div className="rounded-xl border p-6 text-red-500">
        {error}
      </div>
    );

  return (
    <div className="rounded-xl border p-6 space-y-3">
      <div className="flex items-center justify-between">
        <h2 className="text-xl font-semibold">LeetCode</h2>

        <button
          onClick={handleSync}
          disabled={syncing}
          className="rounded bg-green-600 px-3 py-2 text-white hover:bg-green-700 disabled:opacity-50"
        >
          {syncing ? "Syncing..." : "Sync"}
        </button>
      </div>

      <p>Problems Solved: {profile?.solved_problems}</p>
      <p>Easy: {profile?.easy_solved_problems}</p>
      <p>Medium: {profile?.medium_solved_problems}</p>
      <p>Hard: {profile?.hard_solved_problems}</p>

      <hr />

      <p>Contest Rating: {profile?.contest_rating}</p>
      <p>Contest Count: {profile?.contest_count}</p>
      <p>Contest Rank: {profile?.contest_ranking}</p>

      <hr />

      <p>Current Streak: {profile?.current_streak}</p>
      <p>Best Streak: {profile?.max_streak_current_year}</p>

      <p className="text-sm text-gray-500">
        Last Synced: {profile?.last_synced}
      </p>
    </div>
  );
};

export default LeetCodeCard;