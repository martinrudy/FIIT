import { StyleSheet, Text, View } from "react-native";
import RecipeDetail from "../components/Recipes/RecipeDetail";
import { RootStackScreenProps, RouteNames } from "../types/TNavigation";

const RecipeDetailScreen = ({
  route,
}: RootStackScreenProps<RouteNames.RecipeDetail>) => {
  const { recipe } = route.params;
  return (
    <View style={styles.container}>
      <RecipeDetail recipe={recipe} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 16,
    flex: 1,
  },
});

export default RecipeDetailScreen;
