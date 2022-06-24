import { AxiosError } from "axios";
import { FC } from "react";
import { StyleSheet, View, Text, ScrollView } from "react-native";
import { useMutation, useQuery, useQueryClient } from "react-query";
import { QUERY_KEYS } from "../../api/api";
import { deleteFood, setFoodCount } from "../../api/food";
import { getIngredients } from "../../api/recipe";
import { ID_FALLBACK } from "../../constants/Constants";
import { useRefrigeratorInUse } from "../../hooks/useRefrigeratorInUse";
import { TIngredientsGetResponse } from "../../types/TFood";
import { TRecipe } from "../../types/TRecipe";
import { removeFromFoodCache, updateFoodCache } from "../../utils/cacheUtils";
import Button from "../common/Button";
import Spinner from "../common/Spinner";
import Error from "../common/Error";

type Props = {
  recipe: TRecipe;
};

const RecipeDetail: FC<Props> = ({ recipe }) => {
  const { title, text, items } = recipe;

  return (
    <ScrollView contentContainerStyle={styles.container}>
      <Text style={styles.title}>{title}</Text>
      {items.map(({ id, item_count, title }) => (
        <Text
          key={id}
          style={styles.ingredientText}
        >{`${item_count}x ${title}`}</Text>
      ))}
      <Text style={styles.text}>{text}</Text>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 16,
    marginBottom: 8,
  },
  title: {
    fontSize: 28,
    marginBottom: 8,
  },
  ingredientText: {
    fontSize: 18,
  },
  text: {
    fontSize: 16,
    marginTop: 8,
  },
  buttonContainer: {
    flexDirection: "row",
    marginTop: 16,
  },
  doneButton: {
    marginRight: 8,
  },
  noteText: {
    flex: 1,
    fontSize: 10,
    color: "gray",
  },
});

export default RecipeDetail;
