import { FC } from "react";
import { FlatList, ListRenderItem, StyleSheet, Text } from "react-native";
import { TRefrigerator, TRefrigerators } from "../../types/TRefrigerator";
import RefrigeratorListItem from "./RefrigeratorListItem";
import Button from "../common/Button";
import { AntDesign } from "@expo/vector-icons";
import { useNavigation } from "@react-navigation/native";
import { NativeStackNavigationProp } from "@react-navigation/native-stack";
import { RootStackParamList, RouteNames } from "../../types/TNavigation";

const renderItem: ListRenderItem<TRefrigerator> = (listRenderItem) => {
  return <RefrigeratorListItem refrigerator={listRenderItem.item} />;
};

type Props = {
  refrigerators: TRefrigerators;
  isRefreshing: boolean;
  onRefresh: () => void;
};

const RefrigeratorList: FC<Props> = ({
  refrigerators: recipes,
  isRefreshing,
  onRefresh,
}) => {
  const navigation =
    useNavigation<NativeStackNavigationProp<RootStackParamList>>();

  const onAddRefrigeratorPress = () => {
    navigation.push(RouteNames.AddRefrigerator);
  };

  const onJoinVideoConference = () => {
    navigation.push(RouteNames.VideoCall);
  };

  return (
    <FlatList
      data={recipes}
      renderItem={renderItem}
      ListEmptyComponent={
        <Text style={styles.emptyText}>
          No refrigerators? This has to be a bug! :)
        </Text>
      }
      contentContainerStyle={styles.container}
      refreshing={isRefreshing}
      onRefresh={onRefresh}
      ListFooterComponent={
        <>
          <Button
            text="Add new refrigerator"
            onPress={onAddRefrigeratorPress}
            style={styles.addRefrigeratorButton}
            trailingIcon={(color) => (
              <AntDesign name="pluscircleo" size={20} color={color} />
            )}
          />
          <Button
            text="Join video conference"
            onPress={onJoinVideoConference}
            trailingIcon={(color) => (
              <AntDesign name="videocamera" size={20} color={color} />
            )}
          />
        </>
      }
    />
  );
};

const styles = StyleSheet.create({
  container: {
    justifyContent: "center",
  },
  emptyText: {
    margin: 16,
  },
  addRefrigeratorButton: {
    marginVertical: 8,
  },
});

export default RefrigeratorList;
