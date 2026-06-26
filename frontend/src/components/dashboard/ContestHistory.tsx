import type { Dispatch, SetStateAction } from "react";

import {
  syncLeetCodeContests,
  syncCodeforcesContests,
} from "../../api/contest";

import type { LeetCodeContest } from "../../types/leetcode";
import type { CodeforcesContest } from "../../types/codeforces";

import SectionCard from "../common/SectionCard";
import Button from "../common/Button";
import { toast } from "sonner";
interface ContestHistoryProps {
  leetcode: LeetCodeContest[];
  codeforces: CodeforcesContest[];
  loading: boolean;

  setLeetcode: Dispatch<SetStateAction<LeetCodeContest[]>>;
  setCodeforces: Dispatch<SetStateAction<CodeforcesContest[]>>;
}

const ContestHistory = ({
  leetcode,
  codeforces,
  setLeetcode,
  setCodeforces,
}: ContestHistoryProps) => {
  const handleLeetCodeSync = async () => {
  try {
    const contests = await syncLeetCodeContests();

    setLeetcode(contests);

    toast.success("LeetCode contests synced successfully!");
  } catch {
    toast.error("Failed to sync LeetCode contests.");
  }
};

  const handleCodeforcesSync = async () => {
  try {
    const contests = await syncCodeforcesContests();

    setCodeforces(contests);

    toast.success("Codeforces contests synced successfully!");
  } catch {
    toast.error("Failed to sync Codeforces contests.");
  }
};

  return (
    <div className="space-y-8">
      <SectionCard
        title="LeetCode Contests"
        action={
          <Button onClick={handleLeetCodeSync}>
            Sync
          </Button>
        }
      >
        <table className="w-full text-left">
          <thead>
            <tr className="border-b border-zinc-700">
              <th className="pb-3">Contest</th>
              <th className="pb-3">Solved</th>
              <th className="pb-3">Rating</th>
              <th className="pb-3">Rank</th>
            </tr>
          </thead>

          <tbody>
            {leetcode.map((contest) => (
              <tr
                key={contest.id}
                className="border-b border-zinc-800 hover:bg-zinc-900"
              >
                <td className="py-3">{contest.contest_name}</td>
                <td className="py-3">
                  {contest.problems_solved}/{contest.total_problems}
                </td>
                <td className="py-3">{contest.rating}</td>
                <td className="py-3">{contest.ranking}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </SectionCard>

      <SectionCard
        title="Codeforces Contests"
        action={
          <Button onClick={handleCodeforcesSync}>
            Sync
          </Button>
        }
      >
        <table className="w-full text-left">
          <thead>
            <tr className="border-b border-zinc-700">
              <th className="pb-3">Contest</th>
              <th className="pb-3">Rank</th>
              <th className="pb-3">Old Rating</th>
              <th className="pb-3">New Rating</th>
            </tr>
          </thead>

          <tbody>
            {codeforces.map((contest) => (
              <tr
                key={contest.id}
                className="border-b border-zinc-800 hover:bg-zinc-900"
              >
                <td className="py-3">{contest.contest_name}</td>
                <td className="py-3">{contest.rank}</td>
                <td className="py-3">{contest.old_rating}</td>
                <td className="py-3">{contest.new_rating}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </SectionCard>
    </div>
  );
};

export default ContestHistory;