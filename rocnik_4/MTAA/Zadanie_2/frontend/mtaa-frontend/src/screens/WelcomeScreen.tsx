import { Image, StyleSheet, Text, View } from "react-native";
import { RootTabScreenProps } from "../types/TNavigation";
import { RouteNames } from "../types/TNavigation";
import StyledSafeAreaView from "../components/common/SafeAreaView";
import FoodImageSrc from "../assets/food.png";
import Button from "../components/common/Button";
import { AntDesign } from "@expo/vector-icons";

const WelcomeScreen = ({
  navigation,
}: RootTabScreenProps<RouteNames.Recipes>) => {
  const onNextButtonPress = () => {
    navigation.push(RouteNames.Login);
  };

  return (
    <StyledSafeAreaView>
      <Image source={FoodImageSrc} style={styles.image} />
      <View style={styles.contentContainer}>
        <Text style={styles.title}>Welcome to Intelligent Refrigerator</Text>
        <Text style={styles.description}>
          We can help you organize your fridge and recommend meaningful recipes.
        </Text>
        <View style={styles.buttonContainer}>
          <Button
            text="Get started"
            onPress={onNextButtonPress}
            trailingIcon={(color) => (
              <AntDesign name="arrowright" size={24} color={color} />
            )}
          />
        </View>
      </View>
    </StyledSafeAreaView>
  );
};

const styles = StyleSheet.create({
  contentContainer: {
    padding: 24,
    backgroundColor: "white",
  },
  image: {
    height: 256,
    marginTop: 64,
  },
  title: {
    fontSize: 32,
  },
  description: {
    marginTop: 16,
  },
  buttonContainer: {
    flexDirection: "row",
    marginTop: 24,
  },
});

export default WelcomeScreen;
