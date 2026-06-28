import axios from "axios";

export const apiClient = axios.create({
  baseURL: "https://verdict-uhvt.vercel.app",
  withCredentials: true,
});
