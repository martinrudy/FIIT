import { useNavigation } from "@react-navigation/native";
import { FC, useCallback } from "react";
import { StyleSheet } from "react-native";
import { FlatList, ListRenderItem, Text } from "react-native";
import { TIngredient, TIngredients } from "../../types/TFood";
import Button from "../common/Button";
import FoodListItem from "./FoodListItem";
import { AntDesign } from "@expo/vector-icons";
import { BottomTabNavigationProp } from "@react-navigation/bottom-tabs";
import { RootTabParamList, RouteNames } from "../../types/TNavigation";

type Props = {
  ingredients: TIngredients;
  onRefresh: () => void;
  isRefreshing: boolean;
  refrigeratorId: number;
};

const FoodList: FC<Props> = ({
  ingredients,
  onRefresh,
  isRefreshing,
  refrigeratorId,
}) => {
  const navigation = useNavigation<BottomTabNavigationProp<RootTabParamList>>();

  const renderItem: ListRenderItem<TIngredient> = useCallback(
    (listRenderItem) => {
      return (
        <FoodListItem
          ingredient={listRenderItem.item}
          refrigeratorId={refrigeratorId}
        />
      );
    },
    [refrigeratorId]
  );

  const onAddFoodPress = () => {
    navigation.jumpTo(RouteNames.Search);
  };

  return (
    <FlatList
      data={ingredients}
      renderItem={renderItem}
      ListEmptyComponent={
        <Text style={styles.emptyText}>No ingredients yet :(. Add some.</Text>
      }
      contentContainerStyle={styles.container}
      onRefresh={onRefresh}
      refreshing={isRefreshing}
      ListFooterComponent={
        <Button
          text="Add new food"
          onPress={onAddFoodPress}
          style={styles.addFootButton}
          trailingIcon={(color) => (
            <AntDesign name="pluscircleo" size={20} color={color} />
          )}
        />
      }
      keyExtractor={(item) => item.foodType_id.toString()}
    />
  );
};

const styles = StyleSheet.create({
  container: {
    justifyContent: "center",
    padding: 16,
  },
  emptyText: {
    margin: 16,
  },
  separator: {
    height: 20,
  },
  addFootButton: {
    marginTop: 8,
  },
});

export default FoodList;
