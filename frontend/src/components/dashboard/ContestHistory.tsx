import { useEffect, useState } from "react";
import {
  getLeetCodeContests,
  syncLeetCodeContests,
  getCodeforcesContests,
  syncCodeforcesContests,
} from "../../api/contest";
import type { LeetCodeContest } from "../../types/leetcode";
import type { CodeforcesContest } from "../../types/codeforces";

const ContestHistory = () => {
  const [leetcode, setLeetcode] = useState<LeetCodeContest[]>([]);
  const [codeforces, setCodeforces] = useState<CodeforcesContest[]>([]);
  const [loading, setLoading] = useState(true);

  const fetchContests = async () => {
    try {
      const [lc, cf] = await Promise.all([
        getLeetCodeContests(),
        getCodeforcesContests(),
      ]);

      setLeetcode(lc);
      setCodeforces(cf);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchContests();
  }, []);

  const handleLeetCodeSync = async () => {
    const contests = await syncLeetCodeContests();
    setLeetcode(contests);
  };

  const handleCodeforcesSync = async () => {
    const contests = await syncCodeforcesContests();
    setCodeforces(contests);
  };

  if (loading) {
    return (
      <div className="rounded-xl border p-6">
        Loading contests...
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* LeetCode */}
      <div className="rounded-xl border p-6">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-xl font-semibold">LeetCode Contests</h2>

          <button
            onClick={handleLeetCodeSync}
            className="rounded bg-green-600 px-3 py-2 text-white"
          >
            Sync
          </button>
        </div>

        <table className="w-full text-left">
          <thead>
            <tr>
              <th>Contest</th>
              <th>Solved</th>
              <th>Rating</th>
              <th>Rank</th>
            </tr>
          </thead>

          <tbody>
            {leetcode.map((contest) => (
              <tr key={contest.id}>
                <td>{contest.contest_name}</td>
                <td>
                  {contest.problems_solved}/{contest.total_problems}
                </td>
                <td>{contest.rating}</td>
                <td>{contest.ranking}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Codeforces */}
      <div className="rounded-xl border p-6">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="text-xl font-semibold">Codeforces Contests</h2>

          <button
            onClick={handleCodeforcesSync}
            className="rounded bg-green-600 px-3 py-2 text-white"
          >
            Sync
          </button>
        </div>

        <table className="w-full text-left">
          <thead>
            <tr>
              <th>Contest</th>
              <th>Rank</th>
              <th>Old Rating</th>
              <th>New Rating</th>
            </tr>
          </thead>

          <tbody>
            {codeforces.map((contest) => (
              <tr key={contest.id}>
                <td>{contest.contest_name}</td>
                <td>{contest.rank}</td>
                <td>{contest.old_rating}</td>
                <td>{contest.new_rating}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ContestHistory;