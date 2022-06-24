import { StyleSheet, View, Text } from "react-native";
import Colors from "../../constants/Colors";
import useColorScheme from "../../hooks/useColorScheme";
import { MaterialIcons } from "@expo/vector-icons";

const Error = () => {
  const colorScheme = useColorScheme();
  return (
    <View style={styles.container}>
      <MaterialIcons
        name="error-outline"
        size={32}
        color={Colors[colorScheme].text}
      />
      <Text style={styles.text}>Error fetching data :(</Text>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  text: {
    marginTop: 16,
    fontSize: 16,
  },
});

export default Error;
