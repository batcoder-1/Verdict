import axios from "axios";

export const apiClient = axios.create({
  baseURL: "https://verdict-8qeq.onrender.com/cp_analyzer",
  withCredentials: true,
});
