import { AxiosError } from "axios";
import { FC } from "react";
import { StyleSheet, Text, View } from "react-native";
import { useMutation, useQueryClient } from "react-query";
import { QUERY_KEYS } from "../../api/api";
import { deleteRefrigerator, selectRefrigerator } from "../../api/refrigerator";
import { ID_FALLBACK } from "../../constants/Constants";
import { useUserInfo } from "../../contexts/UserInfoContext";
import { TRefrigerator } from "../../types/TRefrigerator";
import Button from "../common/Button";

type Props = {
  refrigerator: TRefrigerator;
};

const RefrigeratorListItem: FC<Props> = ({ refrigerator }) => {
  const { id, name, in_use } = refrigerator;

  const { userId } = useUserInfo();
  const queryClient = useQueryClient();

  const selectMutation = useMutation(
    selectRefrigerator(userId ?? ID_FALLBACK),
    {
      onSuccess: async () => {
        queryClient.invalidateQueries(QUERY_KEYS.refrigerators);
      },
      onError: (error: AxiosError) => {},
    }
  );

  const deleteMutation = useMutation(deleteRefrigerator, {
    onSuccess: () => {
      queryClient.invalidateQueries(QUERY_KEYS.refrigerators);
    },
    onError: (error: AxiosError) => {},
  });

  const onSelectPress = () => {
    selectMutation.mutate(id);
  };

  const onDeletePress = () => {
    deleteMutation.mutate(id);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>{name}</Text>
      <View style={styles.buttonContainer}>
        {in_use ? (
          <>
            <Text>Active</Text>
          </>
        ) : (
          <>
            <Button text="Select" onPress={onSelectPress} />
            <Button
              text="Delete"
              onPress={onDeletePress}
              style={styles.deleteButton}
            />
          </>
        )}
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    padding: 16,
    backgroundColor: "lightgrey",
    marginBottom: 8,
  },
  title: {
    fontSize: 18,
  },
  buttonContainer: {
    flexDirection: "row",
    marginTop: 16,
  },
  deleteButton: {
    marginHorizontal: 16,
    backgroundColor: "#aa0000",
  },
});

export default RefrigeratorListItem;
