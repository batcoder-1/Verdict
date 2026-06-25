import { apiClient } from "./client";

export interface TokenResponse {
  access_token: string;
  token_type: string;
}

export async function login(
  username: string,
  password: string
): Promise<void> {
  const formData = new URLSearchParams();

  formData.append("username", username);
  formData.append("password", password);

  await apiClient.post(
    "/login",
    formData,
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }
  );
}

export async function signup(
  username: string,
  password: string
): Promise<TokenResponse> {
  const formData = new URLSearchParams();

  formData.append("username", username);
  formData.append("password", password);

  const response = await apiClient.post<TokenResponse>(
    "/signup",
    formData,
    {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    }
  );

  return response.data;
}
export async function logout(): Promise<void> {
  await apiClient.post("/logout");
}