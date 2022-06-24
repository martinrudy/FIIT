import { StyleSheet, Text, View } from "react-native";
import Button from "../components/common/Button";
import RefrigeratorListContainer from "../components/Refrigerators/RefrigeratorList.container";
import { useUserInfo } from "../contexts/UserInfoContext";

const OptionsScreen = () => {
  const { setUserId } = useUserInfo();

  const onLogOutPress = () => {
    setUserId(null);
  };

  return (
    <>
      <View style={styles.container}>
        <Text style={styles.title}>Switch refrigerator</Text>
        <RefrigeratorListContainer />
      </View>
      <Button text="Log out" onPress={onLogOutPress} />
    </>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 16,
    flex: 1,
  },
  title: {
    fontSize: 22,
    marginBottom: 16,
  },
});

export default OptionsScreen;
