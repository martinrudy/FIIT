import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { RootStackParamList } from "../types/TNavigation";
import LoginScreen from "../screens/LoginScreen";
import RegisterScreen from "../screens/RegisterScreen";
import WelcomeScreen from "../screens/WelcomeScreen";
import { RouteNames } from "../types/TNavigation";
import BottomTabNavigator from "./BottomTabNavigator";
import { useUserInfo } from "../contexts/UserInfoContext";
import VideoCallScreen from "../screens/VideoCallScreen";
import AddRefrigeratorScreen from "../screens/AddRefrigeratorScreen";
import RecipeDetailScreen from "../screens/RecipeDetailScreen";

const Stack = createNativeStackNavigator<RootStackParamList>();

const StackNavigator = () => {
  const { userId } = useUserInfo();

  return (
    <Stack.Navigator>
      {userId && (
        <Stack.Screen
          name={RouteNames.Home}
          component={BottomTabNavigator}
          options={{ headerShown: false }}
        />
      )}
      <Stack.Screen
        name={RouteNames.Welcome}
        component={WelcomeScreen}
        options={{ headerShown: false }}
      />
      <Stack.Screen
        name={RouteNames.Register}
        component={RegisterScreen}
        options={{ headerShown: false }}
      />
      <Stack.Screen
        name={RouteNames.Login}
        component={LoginScreen}
        options={{ headerShown: false }}
      />
      <Stack.Screen name={RouteNames.VideoCall} component={VideoCallScreen} />
      <Stack.Screen
        name={RouteNames.AddRefrigerator}
        component={AddRefrigeratorScreen}
      />
      <Stack.Screen
        name={RouteNames.RecipeDetail}
        component={RecipeDetailScreen}
      />
    </Stack.Navigator>
  );
};

export default StackNavigator;
