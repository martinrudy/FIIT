import { BottomTabScreenProps } from "@react-navigation/bottom-tabs";
import {
  CompositeScreenProps,
  NavigatorScreenParams,
} from "@react-navigation/native";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { TRecipe } from "./TRecipe";

export enum RouteNames {
  Home = "Home",
  Welcome = "Welcome",
  Login = "Login",
  Register = "Register",
  Recipes = "Recipes",
  RecipeDetail = "Recipe detail",
  Ingredients = "Ingredients",
  Search = "Search",
  Options = "Options",
  VideoCall = "Video call",
  AddRefrigerator = "Add refrigerator",
}

declare global {
  namespace ReactNavigation {
    interface RootParamList extends RootStackParamList {}
  }
}

export type RootStackParamList = {
  [RouteNames.Welcome]: undefined;
  [RouteNames.Register]: undefined;
  [RouteNames.Login]: undefined;
  [RouteNames.Home]: NavigatorScreenParams<RootTabParamList> | undefined;
  [RouteNames.VideoCall]: undefined;
  [RouteNames.AddRefrigerator]: undefined;
  [RouteNames.RecipeDetail]: { recipe: TRecipe };
};

export type RootStackScreenProps<Screen extends keyof RootStackParamList> =
  NativeStackScreenProps<RootStackParamList, Screen>;

export type RootTabParamList = {
  [RouteNames.Recipes]: undefined;
  [RouteNames.Ingredients]: undefined;
  [RouteNames.Search]: undefined;
  [RouteNames.Options]: undefined;
};

export type RootTabScreenProps<Screen extends keyof RootTabParamList> =
  CompositeScreenProps<
    BottomTabScreenProps<RootTabParamList, Screen>,
    NativeStackScreenProps<RootStackParamList>
  >;
