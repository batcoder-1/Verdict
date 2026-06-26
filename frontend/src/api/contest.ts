import {apiClient} from "./client";
import type {
  LeetCodeContest,
} from "../types/leetcode";
import type {
  CodeforcesContest,
} from "../types/codeforces";

export const getLeetCodeContests = async (): Promise<LeetCodeContest[]> => {
  const response = await apiClient.get("/profile/leetcode/contest");
  return response.data;
};

export const syncLeetCodeContests = async (): Promise<LeetCodeContest[]> => {
  const response = await apiClient.post("/profile/leetcode/contest/sync");
  return response.data;
};

export const getCodeforcesContests = async (): Promise<CodeforcesContest[]> => {
  const response = await apiClient.get("/profile/codeforces/contest");
  return response.data;
};

export const syncCodeforcesContests = async (): Promise<CodeforcesContest[]> => {
  const response = await apiClient.post("/profile/codeforces/contest/sync");
  return response.data;
};