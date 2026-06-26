import {apiClient} from "./client";
import  type {LeetCodeProfile}  from "../types/leetcode";

export const getLeetCodeProfile = async (): Promise<LeetCodeProfile> => {
  const response = await apiClient.get("/profile/leetcode");
  return response.data;
};

export const syncLeetCodeProfile = async (): Promise<LeetCodeProfile> => {
  const response = await apiClient.post("/profile/leetcode/sync");
  return response.data;
};