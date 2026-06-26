export interface LeetCodeProfile {
  user_id: string;
  solved_problems: number | null;
  hard_solved_problems: number | null;
  medium_solved_problems: number | null;
  easy_solved_problems: number | null;
  unsolved_problems: number | null;
  ranking: number | null;
  contest_count: number | null;
  contest_rating: number | null;
  contest_ranking: number | null;
  contest_percentage: number | null;
  max_streak_current_year: number | null;
  current_streak: number | null;
  last_synced: string | null;
}

export interface LeetCodeContest {
  id: number;
  user_id: string;
  contest_name: string | null;
  problems_solved: number | null;
  total_problems: number | null;
  rating: number | null;
  ranking: number | null;
  finishTime: string | null;
  last_synced: string | null;
}