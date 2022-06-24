import { StyleSheet, View } from "react-native";
import { RootTabScreenProps } from "../types/TNavigation";
import { RouteNames } from "../types/TNavigation";
import RecipesListContainer from "../components/Recipes/RecipesList.container";
import { useUserInfo } from "../contexts/UserInfoContext";

const RecipesScreen = ({
  navigation,
}: RootTabScreenProps<RouteNames.Recipes>) => {
  return (
    <View style={styles.container}>
      <RecipesListContainer />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
  },
});

export default RecipesScreen;
