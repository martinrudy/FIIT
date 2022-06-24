import axios from "axios";
import { API_URL } from "../constants/Constants";
import {
  TRefrigeratorInput,
  TRefrigeratorsGetResponse,
} from "../types/TRefrigerator";

export const getRefrigerators = (userId: number) => async () => {
  const response = await axios.get<TRefrigeratorsGetResponse>(
    `${API_URL}/users/${userId}/refrigerators`
  );
  return response.data;
};

export const addRefrigerator =
  (userId: number) => async (input: TRefrigeratorInput) => {
    await axios.post(`${API_URL}/users/${userId}/refrigerators`, input);
  };

export const selectRefrigerator =
  (userId: number) => async (refrigeratorId: number) => {
    await axios.patch(
      `${API_URL}/user/${userId}/refrigerator/${refrigeratorId}`
    );
  };

export const deleteRefrigerator = async (refrigeratorId: number) => {
  await axios.delete(`${API_URL}/refrigerators/${refrigeratorId}`);
};
