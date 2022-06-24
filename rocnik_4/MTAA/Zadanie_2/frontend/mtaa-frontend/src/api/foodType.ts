import axios from "axios";
import { API_URL } from "../constants/Constants";
import { TFoodTypesGetResponse } from "../types/TFoodType";

export const getFoodTypes = async () => {
  const response = await axios.get<TFoodTypesGetResponse>(
    `${API_URL}/foodTypes`
  );
  return response.data;
};
