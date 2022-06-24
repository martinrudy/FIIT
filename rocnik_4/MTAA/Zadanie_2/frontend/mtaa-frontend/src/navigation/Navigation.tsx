import { NavigationContainer } from "@react-navigation/native";
import { useUserInfo } from "../contexts/UserInfoContext";
import StackNavigator from "./StackNavigator";

const Navigation = () => {
  const { isLoading } = useUserInfo();

  if (isLoading) {
    return null;
  }

  return (
    <NavigationContainer>
      <StackNavigator />
    </NavigationContainer>
  );
};

export default Navigation;
