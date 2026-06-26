export interface CodeforcesProfile {
  id: string;
  firstname: string | null;
  lastname: string | null;
  rating: number | null;
  max_rating: number | null;
  rank: string | null;
  max_rank: string | null;
  country: string | null;
  friendsCount: number | null;
  last_synced: string | null;
  current_streak: number | null;
  current_year_longest_streak: number | null;
  last_submission_id: number | null;
}

export interface CodeforcesContest {
  id: number;
  user_id: string;
  contest_name: string | null;
  rank: number | null;
  old_rating: number | null;
  new_rating: number | null;
  contest_date: string | null;
  contest_id: number | null;
  last_synced: string | null;
}