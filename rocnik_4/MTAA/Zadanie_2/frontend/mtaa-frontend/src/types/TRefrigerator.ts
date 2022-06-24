export type TRefrigerator = {
  id: number;
  name: string;
  user_id: number;
  in_use: boolean;
};

export type TRefrigerators = TRefrigerator[];

export type TRefrigeratorsGetResponse = TRefrigerators;

export type TRefrigeratorInput = Pick<TRefrigerator, "name">;
