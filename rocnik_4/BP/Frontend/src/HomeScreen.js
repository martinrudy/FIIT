import { StyleSheet, Text, View, Button } from "react-native";
import * as DocumentPicker from "expo-document-picker";
import * as FileSystem from 'expo-file-system';
import axios from "axios";

const HomeScreen = ({ navigation }) => {
    const handleDocumentSelection = async () => {
      let result = await DocumentPicker.getDocumentAsync({});
      //console.log(result);
      FileSystem.readAsStringAsync(result.uri).then(async (cUri) => {
        let string = cUri.replace(/\"/g, "");
        let arr = string.split("\n");
        let headers = arr[0].split(",");
        let objects = []
        for (let i = 1; i < arr.length - 1; i++) {
  
          if(arr[i] === ""){
            break;
          }
  
          let str = arr[i]
          let obj = {}
  
          let values = str.split(",")
          for (let j = 0; j < headers.length; j++){
            obj[headers[j]] = values[j];
          }
          let json = JSON.parse(JSON.stringify(obj))
          objects.push(json);
        }
        //console.log(objects)
        const response = await axios.post("http://192.168.68.103:5000/pressure", objects);
        console.log(objects)
      });
    }
    return (
      <View style={styles.container}>
          <Button
            title="Set config"
            onPress={() =>
              navigation.navigate('Config')
            }
          />
          <Text> </Text>
          <Button
            title="Pick blood pressure file"
            onPress={handleDocumentSelection}
            style={styles.buttonContainer}
          />
        </View>
    );
};
const styles = StyleSheet.create({
    container: {
      flex: 1,
      backgroundColor: "#fff",
      alignItems: "center",
      justifyContent: "center",
    },
    containerInput: {
      borderColor: "black",
      borderWidth: 2,
      fontSize: 17,
      margin: 8,
      width: 200,
    },
    buttonContainer: {
      flexDirection: "row",
      marginTop: 32,
      marginBottom: 32,
      alignItems: "center",
      justifyContent: "space-between",
    },
});

export default HomeScreen;