export interface User {
  id: string;
  username: string;
  isActive: boolean;
  leetcode_handle: string | null;
  codeforces_handle: string | null;
}