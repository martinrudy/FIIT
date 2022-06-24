import { useNavigation } from "@react-navigation/native";
import { NativeStackNavigationProp } from "@react-navigation/native-stack";
import { FC } from "react";
import { FlatList, ListRenderItem, StyleSheet, Text } from "react-native";
import { RootStackParamList, RouteNames } from "../../types/TNavigation";
import { TRecipe, TRecipes } from "../../types/TRecipe";
import Button from "../common/Button";
import RecipesListItem from "./RecipesListItem";

const renderItem: ListRenderItem<TRecipe> = (listRenderItem) => {
  return <RecipesListItem recipe={listRenderItem.item} />;
};

type Props = {
  recipes: TRecipes;
  isRefreshing: boolean;
  onRefresh: () => void;
};

const RecipeList: FC<Props> = ({ recipes, isRefreshing, onRefresh }) => (
  <FlatList
    data={recipes}
    renderItem={renderItem}
    ListEmptyComponent={<Text style={styles.emptyText}>No recipes yet :(</Text>}
    contentContainerStyle={styles.container}
    refreshing={isRefreshing}
    onRefresh={onRefresh}
    keyExtractor={(item) => item.id.toString()}
  />
);

const styles = StyleSheet.create({
  container: {
    justifyContent: "center",
  },
  emptyText: {
    margin: 16,
  },
});

export default RecipeList;
