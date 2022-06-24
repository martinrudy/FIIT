export type TLoginPostRequest = {
  email: string;
  password: string;
};

export type TLoginPostRequestResponse = {
  id: number;
};

export type TRegisterPostRequest = {
  name: string;
  email: string;
  password: string;
  fridge_name: string;
};

export type TRegisterForm = TRegisterPostRequest & {
  passwordAgain: string;
};
