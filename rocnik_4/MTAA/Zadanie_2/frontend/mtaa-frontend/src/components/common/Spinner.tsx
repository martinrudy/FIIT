import { ActivityIndicator, StyleSheet, View, Text } from "react-native";
import Colors from "../../constants/Colors";
import useColorScheme from "../../hooks/useColorScheme";

const Spinner = () => {
  const colorScheme = useColorScheme();
  return (
    <View style={styles.container}>
      <ActivityIndicator color="black" />
      <Text style={styles.text}>Loading...</Text>
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
  },
});

export default Spinner;
