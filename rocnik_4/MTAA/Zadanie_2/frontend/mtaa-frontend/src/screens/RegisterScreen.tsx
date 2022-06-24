import { StyleSheet, Text, View } from "react-native";
import { RootTabScreenProps } from "../types/TNavigation";
import { RouteNames } from "../types/TNavigation";
import StyledSafeAreaView from "../components/common/SafeAreaView";
import StyledTextInput from "../components/common/StyledTextInput";
import Button from "../components/common/Button";
import { useMutation } from "react-query";
import { loginRequest, registerRequest } from "../api/user";
import { Controller, useForm } from "react-hook-form";
import { TLoginPostRequestResponse, TRegisterForm } from "../types/TUser";
import { yupResolver } from "@hookform/resolvers/yup";
import * as yup from "yup";
import { AxiosError } from "axios";
import { useUserInfo } from "../contexts/UserInfoContext";

const MIN_PASSWORD_LENGTH = 8;

const schema = yup
  .object({
    name: yup.string().required(),
    email: yup
      .string()
      .email("Email must be a valid format: example@mail.com")
      .required(),
    password: yup.string().min(MIN_PASSWORD_LENGTH).required(),
    passwordAgain: yup
      .string()
      .required("Confirm your password")
      .oneOf([yup.ref("password"), null], "Passwords must match"),
    fridge_name: yup.string().required("Fridge name is required"),
  })
  .required();

const RegisterScreen = ({
  navigation,
}: RootTabScreenProps<RouteNames.Recipes>) => {
  const { setUserId } = useUserInfo();

  const loginMutation = useMutation(loginRequest, {
    onSuccess: ({ id }: TLoginPostRequestResponse) => {
      setUserId(id);
      navigation.reset({
        index: 0,
        routes: [{ name: RouteNames.Home }],
      });
    },
    onError: (error: AxiosError) => {},
  });

  const registerMutation = useMutation(registerRequest, {
    onSuccess: () => {
      loginMutation.mutate({
        email: getValues("email"),
        password: getValues("password"),
      });
    },
    onError: (error: AxiosError) => {},
  });

  const {
    control,
    handleSubmit,
    formState: { errors },
    getValues,
  } = useForm<TRegisterForm>({
    resolver: yupResolver(schema),
  });

  const onSubmit = (data: TRegisterForm) => {
    registerMutation.mutate(data);
  };

  const loginErrorMessage =
    registerMutation.error?.response?.status === 409
      ? "Email address already in use"
      : "Network request failed";

  const loginError = registerMutation.error ? loginErrorMessage : "";

  return (
    <StyledSafeAreaView>
      <View style={styles.container}>
        <Text style={styles.title}>Register</Text>
        <Controller
          control={control}
          render={({ field: { onChange, onBlur, value, ref } }) => (
            <StyledTextInput
              ref={ref}
              onChangeText={onChange}
              onBlur={onBlur}
              value={value}
              autoCapitalize="none"
              placeholder="Name"
              style={{ marginTop: 32 }}
            />
          )}
          name="name"
        />
        <Text style={styles.error}>{errors.name?.message}</Text>
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
              style={{ marginTop: 16 }}
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
              placeholder="Confirm password"
              style={{ marginTop: 16 }}
            />
          )}
          name="passwordAgain"
        />
        <Text style={styles.error}>{errors.passwordAgain?.message}</Text>
        <Controller
          control={control}
          render={({ field: { onChange, onBlur, value, ref } }) => (
            <StyledTextInput
              ref={ref}
              onChangeText={onChange}
              onBlur={onBlur}
              value={value}
              autoCapitalize="none"
              placeholder="Refrigerator name"
              style={{ marginTop: 16 }}
            />
          )}
          name="fridge_name"
        />
        <Text style={styles.error}>{errors.fridge_name?.message}</Text>
        <View style={styles.buttonContainer}>
          <Button
            text="Register"
            isLoading={registerMutation.isLoading && loginMutation.isLoading}
            onPress={handleSubmit(onSubmit)}
          />
        </View>
        <Text style={[styles.error, styles.mainError]}>{loginError}</Text>
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
  },
  error: {
    color: "red",
  },
  mainError: {
    marginTop: 16,
  },
});

export default RegisterScreen;
