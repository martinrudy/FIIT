import { forwardRef } from "react";
import { StyleSheet, TextInput, TextInputProps } from "react-native";

const StyledTextInput = forwardRef<TextInput, TextInputProps>((props, ref) => (
  <TextInput ref={ref} {...props} style={[props.style, styles.container]} />
));

const styles = StyleSheet.create({
  container: {
    borderBottomColor: "black",
    borderBottomWidth: 2,
    fontSize: 17,
    paddingBottom: 8,
  },
});

export default StyledTextInput;
