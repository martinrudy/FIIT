import axios from "axios";
import { API_URL } from "../constants/Constants";
import {
  TFoodDeleteRequestMutationInput,
  TFoodPatchRequestMutationInput,
  TFoodPostRequestMutationInput,
} from "../types/TFood";

export const setFoodCount = async ({
  refrigeratorId,
  foodType_id,
  body,
}: TFoodPatchRequestMutationInput) => {
  await axios.put(
    `${API_URL}/refrigerator/${refrigeratorId}/food/${foodType_id}`,
    body
  );
};

export const addFood = async ({
  refrigeratorId,
  body,
}: TFoodPostRequestMutationInput) => {
  await axios.post(`${API_URL}/refrigerator/${refrigeratorId}/food`, body);
};

export const deleteFood = async ({
  refrigeratorId,
  foodId,
}: TFoodDeleteRequestMutationInput) => {
  await axios.delete(
    `${API_URL}/refrigerator/${refrigeratorId}/food/${foodId}`
  );
};
