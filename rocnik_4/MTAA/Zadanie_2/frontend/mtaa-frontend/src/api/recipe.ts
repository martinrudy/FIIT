import axios from "axios";
import { API_URL } from "../constants/Constants";
import { TIngredientsGetResponse } from "../types/TFood";
import { TRecipesGetResponse } from "../types/TRecipe";

export const getRecipes = (refrigeratorId: number) => async () => {
  const response = await axios.get<TRecipesGetResponse>(
    `${API_URL}/refrigerator/${refrigeratorId}/recipes`
  );
  return response.data;
};

export const getIngredients = (refrigeratorId: number) => async () => {
  const response = await axios.get<TIngredientsGetResponse>(
    `${API_URL}/refrigerator/${refrigeratorId}/food`
  );
  return response.data;
};
