import { apiClient } from "./client";
import type { User } from "../types/user";

export async function getProfile(): Promise<User> {
  const response = await apiClient.get<User>("/profile");
  return response.data;
}

interface UpdateProfileData {
  leetcode_handle?: string;
  codeforces_handle?: string;
}

export async function updateProfile(
  data: UpdateProfileData
): Promise<User> {
  const response = await apiClient.patch<User>("/profile", data);
  return response.data;
}