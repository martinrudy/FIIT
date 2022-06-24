import { Feather, Ionicons, MaterialCommunityIcons } from "@expo/vector-icons";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { RootTabParamList, RootTabScreenProps } from "../types/TNavigation";
import { RouteNames } from "../types/TNavigation";
import Colors from "../constants/Colors";
import RecipesScreen from "../screens/RecipesScreen";
import useColorScheme from "../hooks/useColorScheme";
import IngredientsScreen from "../screens/IngredientsScreen";
import SearchScreen from "../screens/SearchScreen";
import OptionsScreen from "../screens/OptionsScreen";

const BottomTab = createBottomTabNavigator<RootTabParamList>();

const BottomTabNavigator = () => {
  const colorScheme = useColorScheme();

  return (
    <BottomTab.Navigator
      initialRouteName={RouteNames.Recipes}
      screenOptions={{
        tabBarActiveTintColor: Colors[colorScheme].tint,
      }}
    >
      <BottomTab.Screen
        name={RouteNames.Recipes}
        component={RecipesScreen}
        options={({ navigation }: RootTabScreenProps<RouteNames.Recipes>) => ({
          title: RouteNames.Recipes,
          tabBarIcon: ({ color }) => (
            <Feather name="book-open" size={24} color={color} />
          ),
        })}
      />
      <BottomTab.Screen
        name={RouteNames.Ingredients}
        component={IngredientsScreen}
        options={{
          title: RouteNames.Ingredients,
          tabBarIcon: ({ color }) => (
            <MaterialCommunityIcons
              name="fridge-outline"
              size={24}
              color={color}
            />
          ),
        }}
      />
      <BottomTab.Screen
        name={RouteNames.Search}
        component={SearchScreen}
        options={{
          title: RouteNames.Search,
          tabBarIcon: ({ color }) => (
            <Feather name="search" size={24} color={color} />
          ),
        }}
      />
      <BottomTab.Screen
        name={RouteNames.Options}
        component={OptionsScreen}
        options={{
          title: RouteNames.Options,
          tabBarIcon: ({ color }) => (
            <Ionicons name="options-outline" size={24} color={color} />
          ),
        }}
      />
    </BottomTab.Navigator>
  );
};

export default BottomTabNavigator;
