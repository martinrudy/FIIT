export type TFoodType = {
  id: number;
  title: string;
  category: string;
  file_path: string;
};

export type TFoodTypes = TFoodType[];

export type TFoodTypesGetResponse = TFoodTypes;
