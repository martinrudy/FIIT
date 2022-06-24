import axios from "axios";
import { API_URL } from "../constants/Constants";
import {
  TLoginPostRequest,
  TLoginPostRequestResponse,
  TRegisterPostRequest,
} from "../types/TUser";

export const loginRequest = async (body: TLoginPostRequest) => {
  const response = await axios.post<TLoginPostRequestResponse>(
    `${API_URL}/login`,
    body
  );
  return response.data;
};

export const registerRequest = async (body: TRegisterPostRequest) => {
  await axios.post(`${API_URL}/register`, body);
};
