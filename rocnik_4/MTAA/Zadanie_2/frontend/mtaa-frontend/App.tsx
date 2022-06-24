import { StatusBar } from "expo-status-bar";
import { SafeAreaProvider } from "react-native-safe-area-context";
import { QueryClient, QueryClientProvider } from "react-query";
import { UserInfoProvider } from "./src/contexts/UserInfoContext";
import useCachedResources from "./src/hooks/useCachedResources";
import Navigation from "./src/navigation/Navigation";
import { LogBox } from "react-native";

LogBox.ignoreLogs(["Setting a timer"]);

const queryClient = new QueryClient();

const App = () => {
  const isLoadingComplete = useCachedResources();
  if (!isLoadingComplete) {
    return null;
  } else {
    return (
      <QueryClientProvider client={queryClient}>
        <SafeAreaProvider>
          <UserInfoProvider>
            <Navigation />
          </UserInfoProvider>
          <StatusBar />
        </SafeAreaProvider>
      </QueryClientProvider>
    );
  }
};

export default App;
