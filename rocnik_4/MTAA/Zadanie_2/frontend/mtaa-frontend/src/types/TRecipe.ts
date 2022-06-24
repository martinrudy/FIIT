export type TRecipe = {
  id: number;
  title: string;
  text: string;
  items: [{ id: number; item_count: number; title: string }];
};

export type TRecipes = TRecipe[];

export type TRecipesGetResponse = TRecipes;
