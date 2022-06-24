import { FC, ReactElement } from "react";
import {
  ActivityIndicator,
  Pressable,
  StyleProp,
  StyleSheet,
  View,
  ViewStyle,
  Text,
} from "react-native";

type ButtonType = "primary" | "secondary";

const getContainerStyle = (type: ButtonType, pressed: boolean) => {
  if (type === "primary") return { backgroundColor: pressed ? "#777" : "#999" };
  else
    return {
      backgroundColor: "transparent",
    };
};

const getTextStyle = (type: ButtonType, pressed: boolean) => {
  if (type === "primary") return { color: "white" };
  else
    return {
      color: pressed ? "#666" : "#999",
    };
};

type Props = {
  text: string;
  onPress: () => void;
  trailingIcon?: (color: string) => ReactElement;
  isLoading?: boolean;
  type?: "primary" | "secondary";
  style?: StyleProp<ViewStyle>;
};

const Button: FC<Props> = ({
  text,
  onPress,
  trailingIcon,
  isLoading,
  type = "primary",
  style,
}) => (
  <Pressable
    onPress={onPress}
    style={({ pressed }) => [
      getContainerStyle(type, pressed),
      styles.container,
      style,
    ]}
    disabled={isLoading}
  >
    {({ pressed }) => (
      <>
        <Text style={[styles.text, getTextStyle(type, pressed)]}>{text}</Text>
        {isLoading && (
          <ActivityIndicator color="black" style={{ marginLeft: 8 }} />
        )}
        {trailingIcon && (
          <View style={styles.trailingIconWrapper}>
            {trailingIcon("white")}
          </View>
        )}
      </>
    )}
  </Pressable>
);

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    alignItems: "center",
    padding: 8,
  },
  text: {
    color: "white",
    fontWeight: "bold",
    fontSize: 16,
  },
  trailingIconWrapper: {
    marginLeft: 8,
  },
});

export default Button;
