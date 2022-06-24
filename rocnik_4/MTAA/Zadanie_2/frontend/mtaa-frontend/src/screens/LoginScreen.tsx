import { StyleSheet, Text, View } from "react-native";
import { RootTabScreenProps } from "../types/TNavigation";
import { RouteNames } from "../types/TNavigation";
import StyledSafeAreaView from "../components/common/SafeAreaView";
import StyledTextInput from "../components/common/StyledTextInput";
import Button from "../components/common/Button";
import { useMutation } from "react-query";
import { loginRequest } from "../api/user";
import { Controller, useForm } from "react-hook-form";
import { TLoginPostRequest, TLoginPostRequestResponse } from "../types/TUser";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";
import { AxiosError } from "axios";
import { useUserInfo } from "../contexts/UserInfoContext";

const MIN_PASSWORD_LENGTH = 8;

const schema = yup
  .object({
    email: yup
      .string()
      .email("Email must be a valid format: example@mail.com")
      .required(),
    password: yup.string().min(MIN_PASSWORD_LENGTH).required(),
  })
  .required();

const LoginScreen = ({
  navigation,
}: RootTabScreenProps<RouteNames.Recipes>) => {
  const { setUserId: setUserInfo } = useUserInfo();

  const loginMutation = useMutation(loginRequest, {
    onSuccess: ({ id }: TLoginPostRequestResponse) => {
      setUserInfo(id);
      navigation.reset({
        index: 0,
        routes: [{ name: RouteNames.Home }],
      });
    },
    onError: (error: AxiosError) => {},
  });

  const {
    control,
    handleSubmit,
    formState: { errors },
  } = useForm<TLoginPostRequest>({
    resolver: yupResolver(schema),
  });

  const onSubmit = (data: TLoginPostRequest) => {
    loginMutation.mutate(data);
  };

  const onRegisterPress = () => {
    navigation.push(RouteNames.Register);
  };

  const loginErrorMessage =
    loginMutation.error?.response?.status === 404
      ? "Invalid email or password"
      : "Network request failed";

  const loginError = loginMutation.error ? loginErrorMessage : "";

  return (
    <StyledSafeAreaView>
      <View style={styles.container}>
        <Text style={styles.title}>Login</Text>
        <Controller
          control={control}
          render={({ field: { onChange, onBlur, value, ref } }) => (
            <StyledTextInput
              ref={ref}
              onChangeText={onChange}
              onBlur={onBlur}
              value={value}
              autoCapitalize="none"
              placeholder="Email"
              style={{ marginTop: 32 }}
            />
          )}
          name="email"
        />
        <Text style={styles.error}>{errors.email?.message}</Text>
        <Controller
          control={control}
          render={({ field: { onChange, onBlur, value, ref } }) => (
            <StyledTextInput
              ref={ref}
              onChangeText={onChange}
              onBlur={onBlur}
              value={value}
              autoCapitalize="none"
              secureTextEntry
              placeholder="Password"
              style={{ marginTop: 16 }}
            />
          )}
          name="password"
        />
        <Text style={styles.error}>{errors.password?.message}</Text>
        <View style={styles.buttonContainer}>
          <Button
            text="Login"
            isLoading={loginMutation.isLoading}
            onPress={handleSubmit(onSubmit)}
          />
          <Button
            type="secondary"
            text="Create an account"
            onPress={onRegisterPress}
          />
        </View>
        <Text style={[styles.error, styles.loginError]}>{loginError}</Text>
      </View>
    </StyledSafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    padding: 24,
  },
  title: {
    fontSize: 32,
  },
  buttonContainer: {
    flexDirection: "row",
    marginTop: 32,
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

export default LoginScreen;
