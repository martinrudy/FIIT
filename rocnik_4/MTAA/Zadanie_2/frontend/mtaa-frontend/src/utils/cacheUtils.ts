import {
  TFoodPatchRequestMutationInput,
  TIngredientsGetResponse,
  TFoodDeleteRequestMutationInput,
} from "../types/TFood";

export const updateFoodCache =
  (input: TFoodPatchRequestMutationInput) =>
  (old: TIngredientsGetResponse | undefined): TIngredientsGetResponse => {
    return (
      old?.map((food) => {
        if (food.foodType_id === input.foodType_id) {
          return {
            ...food,
            item_count: input.body.item_count,
          };
        } else {
          return food;
        }
      }) ?? []
    );
  };

export const removeFromFoodCache =
  (input: TFoodDeleteRequestMutationInput) =>
  (old: TIngredientsGetResponse | undefined): TIngredientsGetResponse => {
    return old?.filter((food) => food.foodType_id !== input.foodId) ?? [];
  };
