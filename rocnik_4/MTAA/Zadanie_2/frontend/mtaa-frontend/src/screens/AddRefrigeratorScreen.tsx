import { StyleSheet, Text, View } from "react-native";
import { RootTabScreenProps } from "../types/TNavigation";
import { RouteNames } from "../types/TNavigation";
import StyledSafeAreaView from "../components/common/SafeAreaView";
import StyledTextInput from "../components/common/StyledTextInput";
import Button from "../components/common/Button";
import { useMutation, useQueryClient } from "react-query";
import { Controller, useForm } from "react-hook-form";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";
import { AxiosError } from "axios";
import { useUserInfo } from "../contexts/UserInfoContext";
import { addRefrigerator } from "../api/refrigerator";
import { ID_FALLBACK } from "../constants/Constants";
import { QUERY_KEYS } from "../api/api";
import { TRefrigeratorInput } from "../types/TRefrigerator";

const MIN_REFRIGERATOR_NAME_LENGTH = 8;

const schema = yup
  .object({
    name: yup.string().min(MIN_REFRIGERATOR_NAME_LENGTH).required(),
  })
  .required();

const AddRefrigeratorScreen = ({
  navigation,
}: RootTabScreenProps<RouteNames.Recipes>) => {
  const queryClient = useQueryClient();
  const { userId } = useUserInfo();

  const addRefrigeratorMutation = useMutation(
    addRefrigerator(userId ?? ID_FALLBACK),
    {
      onSuccess: () => {
        queryClient.invalidateQueries(QUERY_KEYS.refrigerators);
        navigation.pop();
      },
      onError: (error: AxiosError) => {},
    }
  );

  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<TRefrigeratorInput>({
    resolver: yupResolver(schema),
  });

  const onSubmit = (data: TRefrigeratorInput) => {
    addRefrigeratorMutation.mutate(data);
  };

  const errorMessage = addRefrigeratorMutation.isError
    ? "Network request failed"
    : "";

  return (
    <StyledSafeAreaView>
      <View style={styles.container}>
        <Text style={styles.title}>Add a new refrigerator</Text>
        <Controller
          control={control}
          render={({ field: { onChange, onBlur, value, ref } }) => (
            <StyledTextInput
              ref={ref}
              onChangeText={onChange}
              onBlur={onBlur}
              value={value}
              placeholder="Refrigerator name"
              style={{ marginTop: 32 }}
            />
          )}
          name="name"
        />
        <Text style={styles.error}>{errors.name?.message}</Text>
        <View style={styles.buttonContainer}>
          <Button
            text="Add"
            isLoading={addRefrigeratorMutation.isLoading}
            onPress={handleSubmit(onSubmit)}
          />
        </View>
        <Text style={[styles.error, styles.loginError]}>{errorMessage}</Text>
      </View>
    </StyledSafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    padding: 16,
  },
  title: {
    fontSize: 32,
  },
  buttonContainer: {
    flexDirection: "row",
    marginTop: 8,
    alignItems: "center",
    justifyContent: "space-between",
  },
  error: {
    color: "red",
  },
  loginError: {
    marginTop: 16,
  },
});

export default AddRefrigeratorScreen;
