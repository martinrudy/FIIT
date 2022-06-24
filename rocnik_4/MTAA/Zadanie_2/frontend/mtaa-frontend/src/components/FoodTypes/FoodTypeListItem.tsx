import { AxiosError } from "axios";
import { FC } from "react";
import { StyleSheet, Text, View, Image } from "react-native";
import { useMutation, useQueryClient } from "react-query";
import { QUERY_KEYS } from "../../api/api";
import { addFood } from "../../api/food";
import { API_URL, ID_FALLBACK } from "../../constants/Constants";
import { TFoodPostRequestMutationInput } from "../../types/TFood";
import { TFoodType, TFoodTypesGetResponse } from "../../types/TFoodType";
import Button from "../common/Button";

const updateFoodTypesCache =
  (input: TFoodPostRequestMutationInput) =>
  (old: TFoodTypesGetResponse | undefined): TFoodTypesGetResponse => {
    return (
      old?.filter((foodType) => {
        foodType.id !== input.body.item_id;
      }) ?? []
    );
  };

type Props = {
  foodType: TFoodType;
  refrigeratorId: number;
};

const FoodTypeListItem: FC<Props> = ({ foodType, refrigeratorId }) => {
  const queryClient = useQueryClient();

  const addFoodMutation = useMutation(addFood, {
    onSuccess: () => {},
    onMutate: async (input) => {
      await queryClient.cancelQueries(QUERY_KEYS.foodTypes);
      await queryClient.cancelQueries(QUERY_KEYS.food);
      const previousFood = queryClient.getQueryData<TFoodTypesGetResponse>(
        QUERY_KEYS.recipes
      );
      queryClient.setQueryData<TFoodTypesGetResponse>(
        QUERY_KEYS.foodTypes,
        updateFoodTypesCache(input)
      );
      return previousFood;
    },
    onError: (error: AxiosError, input, context) => {
      queryClient.setQueryData(QUERY_KEYS.foodTypes, context);
    },
    onSettled: () => {
      queryClient.invalidateQueries(QUERY_KEYS.food);
      queryClient.invalidateQueries(QUERY_KEYS.foodTypes);
      queryClient.invalidateQueries(QUERY_KEYS.recipes);
    },
  });

  const onPlusPress = () => {
    addFoodMutation.mutate({
      refrigeratorId: refrigeratorId ?? ID_FALLBACK,
      body: {
        item_id: foodType.id,
        item_count: 1,
      },
    });
  };

  console.log(`${API_URL}/${foodType.file_path}`);

  return (
    <View style={styles.container}>
      <View style={styles.leftContent}>
        <Image
          source={{ uri: `${API_URL}/${foodType.file_path}` }}
          style={styles.image}
        />
        <Text style={styles.title}>{foodType.title}</Text>
        <View style={styles.chip}>
          <Text style={styles.chipText}>{foodType.category}</Text>
        </View>
      </View>
      <Button text="+" onPress={onPlusPress} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 16,
    backgroundColor: "lightgrey",
    marginBottom: 8,
    flexDirection: "row",
    alignItems: "center",
  },
  image: {
    width: 50,
    height: 50,
    marginRight: 8,
  },
  title: {
    fontWeight: "600",
  },
  chip: {
    flexDirection: "row",
    backgroundColor: "grey",
    padding: 6,
    borderRadius: 16,
    marginHorizontal: 8,
  },
  chipText: {
    color: "white",
    fontSize: 12,
    fontWeight: "400",
  },
  leftContent: {
    flex: 1,
    flexDirection: "row",
    alignItems: "center",
  },
});

export default FoodTypeListItem;
