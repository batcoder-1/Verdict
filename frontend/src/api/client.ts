import axios from "axios";

export const apiClient = axios.create({
  baseURL: "https://verdict-8qeq.onrender.com",
  withCredentials: true,
});
