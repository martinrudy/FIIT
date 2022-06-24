import { useNavigation } from "@react-navigation/native";
import { NativeStackNavigationProp } from "@react-navigation/native-stack";
import { FC } from "react";
import { StyleSheet, Text, View } from "react-native";
import { RootStackParamList, RouteNames } from "../../types/TNavigation";
import { TRecipe } from "../../types/TRecipe";
import Button from "../common/Button";

type Props = {
  recipe: TRecipe;
};

const RecipesListItem: FC<Props> = ({ recipe }) => {
  const { title, text, items } = recipe;

  const navigation =
    useNavigation<NativeStackNavigationProp<RootStackParamList>>();

  const onMorePress = () => {
    navigation.push(RouteNames.RecipeDetail, { recipe });
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{title}</Text>
      {items.map(({ id, item_count, title }) => (
        <Text
          key={id}
          style={styles.ingredientText}
        >{`${item_count}x ${title}`}</Text>
      ))}
      <Text style={styles.text} numberOfLines={1}>
        {text}
      </Text>
      <View style={styles.buttonContainer}>
        <Button text="More" onPress={onMorePress} />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 16,
    backgroundColor: "lightgrey",
    marginBottom: 8,
  },
  title: {
    fontSize: 20,
    marginBottom: 8,
  },
  ingredientText: {
    fontSize: 16,
  },
  text: {
    fontSize: 14,
    marginTop: 8,
  },
  buttonContainer: {
    flexDirection: "row",
    marginTop: 16,
  },
});

export default RecipesListItem;
