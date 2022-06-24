import { StyleSheet, View } from "react-native";
import { RootTabScreenProps } from "../types/TNavigation";
import { RouteNames } from "../types/TNavigation";
import FoodListContainer from "../components/Food/FoodList.container";

const IngredientsScreen = ({
  navigation,
}: RootTabScreenProps<RouteNames.Recipes>) => {
  return (
    <View style={styles.container}>
      <FoodListContainer />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
});

export default IngredientsScreen;
