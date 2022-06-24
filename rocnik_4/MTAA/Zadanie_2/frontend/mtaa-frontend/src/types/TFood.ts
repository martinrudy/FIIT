export type TIngredient = {
  category: string;
  item_count: number;
  title: string;
  foodType_id: number;
};

export type TIngredients = TIngredient[];

export type TIngredientsGetResponse = TIngredients;

export type TFoodPatchRequestBody = {
  item_count: number;
};

export type TFoodPatchRequestMutationInput = {
  refrigeratorId: number;
  foodType_id: number;
  body: TFoodPatchRequestBody;
};

export type TFoodPostRequestBody = {
  item_id: number;
  item_count: number;
};

export type TFoodPostRequestMutationInput = {
  refrigeratorId: number;
  body: TFoodPostRequestBody;
};

export type TFoodDeleteRequestMutationInput = {
  refrigeratorId: number;
  foodId: number;
};
