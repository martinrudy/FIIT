import { useState } from "react";
import { StyleSheet, View } from "react-native";
import StyledTextInput from "../components/common/StyledTextInput";
import FoodTypeListContainer from "../components/FoodTypes/FoodTypeList.container";
import { AntDesign } from "@expo/vector-icons";

export default function SearchScreen() {
  const [searchQuery, setSearchQuery] = useState<string>();

  const onChangeText = (text: string) => {
    setSearchQuery(text.toLowerCase());
  };

  return (
    <View style={styles.container}>
      <View style={styles.inputContainer}>
        <AntDesign name="search1" size={24} color="black" />
        <StyledTextInput
          placeholder="Enter food name"
          style={styles.input}
          onChangeText={onChangeText}
          autoCapitalize="none"
        />
      </View>
      <FoodTypeListContainer searchQuery={searchQuery} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    padding: 16,
    flex: 1,
  },
  inputContainer: {
    flexDirection: "row",
    alignItems: "center",
    marginBottom: 16,
  },
  input: {
    marginLeft: 16,
    flex: 1,
  },
});
