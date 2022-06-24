import { FC, useCallback } from "react";
import { FlatList, ListRenderItem, StyleSheet, Text } from "react-native";
import { TFoodType, TFoodTypes } from "../../types/TFoodType";
import FoodTypeListItem from "./FoodTypeListItem";

type Props = {
  foodTypes: TFoodTypes;
  refrigeratorId: number;
  isRefreshing: boolean;
  onRefresh: () => void;
};

const FoodTypeList: FC<Props> = ({
  foodTypes: recipes,
  refrigeratorId,
  isRefreshing,
  onRefresh,
}) => {
  const renderItem: ListRenderItem<TFoodType> = useCallback(
    (listRenderItem) => {
      return (
        <FoodTypeListItem
          refrigeratorId={refrigeratorId}
          foodType={listRenderItem.item}
        />
      );
    },
    [refrigeratorId]
  );

  return (
    <FlatList
      data={recipes}
      renderItem={renderItem}
      ListEmptyComponent={
        <Text style={styles.emptyText}>
          No food types were found. We are sorry :/
        </Text>
      }
      contentContainerStyle={styles.container}
      refreshing={isRefreshing}
      onRefresh={onRefresh}
      keyExtractor={(item) => item.id.toString()}
    />
  );
};

const styles = StyleSheet.create({
  container: {
    justifyContent: "center",
  },
  emptyText: {
    margin: 16,
  },
});

export default FoodTypeList;
