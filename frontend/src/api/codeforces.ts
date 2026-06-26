import {apiClient} from "./client";
import type { CodeforcesProfile } from "../types/codeforces";

export const getCodeforcesProfile = async (): Promise<CodeforcesProfile> => {
  const response = await apiClient.get("/profile/codeforces");
  return response.data;
};

export const syncCodeforcesProfile = async (): Promise<CodeforcesProfile> => {
  const response = await apiClient.post("/profile/codeforces/sync");
  return response.data;
};