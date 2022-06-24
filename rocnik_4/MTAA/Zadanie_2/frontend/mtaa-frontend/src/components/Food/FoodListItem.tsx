import { AxiosError } from "axios";
import { FC } from "react";
import { StyleSheet, Text, View } from "react-native";
import { useMutation, useQueryClient } from "react-query";
import { QUERY_KEYS } from "../../api/api";
import { deleteFood, setFoodCount } from "../../api/food";
import { TIngredient, TIngredientsGetResponse } from "../../types/TFood";
import { removeFromFoodCache, updateFoodCache } from "../../utils/cacheUtils";
import Button from "../common/Button";

type Props = {
  ingredient: TIngredient;
  refrigeratorId: number;
};

const FoodListItem: FC<Props> = ({ ingredient, refrigeratorId }) => {
  const queryClient = useQueryClient();

  const deleteFoodMutation = useMutation(deleteFood, {
    onSuccess: () => {},
    onMutate: async (input) => {
      await queryClient.cancelQueries(QUERY_KEYS.food);
      const previousFood = queryClient.getQueryData<TIngredientsGetResponse>(
        QUERY_KEYS.food
      );
      queryClient.setQueryData<TIngredientsGetResponse>(
        QUERY_KEYS.food,
        removeFromFoodCache(input)
      );
      return previousFood;
    },
    onError: (error: AxiosError, input, context) => {
      queryClient.setQueryData(QUERY_KEYS.food, context);
    },
    onSettled: () => {
      queryClient.invalidateQueries(QUERY_KEYS.food);
      queryClient.invalidateQueries(QUERY_KEYS.recipes);
    },
  });

  const setFoodCountMutation = useMutation(setFoodCount, {
    onSuccess: () => {},
    onMutate: async (input) => {
      await queryClient.cancelQueries(QUERY_KEYS.food);
      const previousFood = queryClient.getQueryData<TIngredientsGetResponse>(
        QUERY_KEYS.food
      );
      queryClient.setQueryData<TIngredientsGetResponse>(
        QUERY_KEYS.food,
        updateFoodCache(input)
      );
      return previousFood;
    },
    onError: (error: AxiosError, input, context) => {
      queryClient.setQueryData(QUERY_KEYS.food, context);
    },
    onSettled: () => {
      queryClient.invalidateQueries(QUERY_KEYS.food);
      queryClient.invalidateQueries(QUERY_KEYS.recipes);
    },
  });

  const onPlusPress = () => {
    setFoodCountMutation.mutate({
      refrigeratorId,
      foodType_id: ingredient.foodType_id,
      body: {
        item_count: ingredient.item_count + 1,
      },
    });
  };

  const onMinusPress = () => {
    if (ingredient.item_count - 1 <= 0) {
      deleteFoodMutation.mutate({
        refrigeratorId,
        foodId: ingredient.foodType_id,
      });
    } else {
      setFoodCountMutation.mutate({
        refrigeratorId,
        foodType_id: ingredient.foodType_id,
        body: {
          item_count: ingredient.item_count - 1,
        },
      });
    }
  };

  return (
    <View style={styles.container}>
      <Text>{ingredient.title}</Text>
      <View style={styles.rightContainer}>
        <Text>{`${ingredient.item_count}x`}</Text>
        <Button
          type="primary"
          text="+"
          onPress={onPlusPress}
          style={styles.plusButton}
        />
        <Button type="primary" text="-" onPress={onMinusPress} />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    backgroundColor: "lightgrey",
    padding: 16,
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: 8,
  },
  rightContainer: {
    flexDirection: "row",
    alignItems: "center",
  },
  plusButton: {
    marginHorizontal: 8,
  },
});

export default FoodListItem;
