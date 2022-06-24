import { StyleSheet, Text, View, TextInput, Button } from "react-native";
import RNBluetoothClassic from "react-native-bluetooth-classic";
import { useEffect, useState, useCallback } from "react";
import axios from "axios";


const Config = ({ navigation, route }) => {
    const [device, setDevice] = useState();
    const [conn, setCon] = useState("Waiting for BT connection");
    const [fileResponse, setFileResponse] = useState([]);
    let isConnected;
  
    // Tries to find and connect to arduino by device name
    // If the arduino is not found, does nothing
    const findArduino = async () => {
      if (device) return;
      try {
        const paired = await RNBluetoothClassic.getBondedDevices();
        for (const device of paired) {
          if (device.name == "RUDYHOBT") {
            setDevice(device);
          }
        }
      } catch (err) {
        console.log(err);
      }
    };
  
    // Try to find and connect to arduino every 5 seconds
    useEffect(() => {
      const interval = setInterval(() => {
        findArduino();
      }, 5000);
      return () => clearInterval(interval);
    }, []);
  
    const readDeviceData = useCallback(async () => {
      if (!device) {
        console.log("Device not available yet");
        return;
      }
      try {
        const message = await device.read();
        //console.log(message)
        if (message) {
          console.log(message);
          if (message.startsWith('{')){
            let obj = JSON.parse(message);
            //console.log(JSON.stringify(objekt));
            const response = await axios.post("http://192.168.68.103:5000/upload", obj);
            const data = response.data;
            if (data.success) {
              console.log("sent data successfully")
            }
          }
        }
      } catch (error) {
        console.log(error);
      }
    }, [device]);
  
    // Read data from device every 1 second if available
    useEffect(() => {
      const interval = setInterval(() => {
        readDeviceData();
      }, 1000);
      return () => clearInterval(interval);
    }, [device]);
  
    // Connect to device when it becomes available
    useEffect(() => {
      (async () => {
        try {
          isConnected = await device.isConnected();
          if (!isConnected) {
            await device.connect();
          }
          else{
            setCon("Connected");
          }
        } catch (error) {
          console.log(error);
        }
      })();
    }, [device]);
  
    const sendDeviceData = useCallback(async (props) => {
      console.log(props)
      if (!device) {
        console.log("Device not available yet");
        return;
      }
      try {
        const message = await device.write(props);
        //console.log(message);
        if (message) {
          console.log("data sent");
        }
      } catch (error) {
        console.log(error);
      }
    }, [device]);
    
    const [measure, onChangeMeasure] = useState("");
    const [send, onChangeSend] = useState("");
    const [tempObj, onChangeObj] = useState("");
    const [oxygen, onChangeOxy] = useState("");
    const [bpm, onChangeBpm] = useState("");
  
    const handleInput = async () => {
      let measMillis = measure*60000;
      let sendMillis = send*60000;
      if(isConnected){
        let msg = {
          "mea": measMillis,
          "snd": sendMillis,
          "tmp": tempObj,
          "oxy": oxygen,
          "bpm": bpm
        }
        sendDeviceData(JSON.stringify(msg))
      }
    }
    return (
      <View style={styles.container}>
          <Text>{conn}</Text>
          <TextInput  style={styles.containerInput}
                      keyboardType={'numeric'}
                      placeholder="Measure minutes"
                      onChangeText={onChangeMeasure}
                      value={measure}
          />
          <TextInput  style={styles.containerInput}
                      keyboardType={'numeric'}
                      placeholder="Send data minutes"
                      onChangeText={onChangeSend}
                      value={send}
          />
          <TextInput  style={styles.containerInput}
                      keyboardType={'numeric'}
                      placeholder="Treshold ObjTemp"
                      onChangeText={onChangeObj}
                      value={tempObj}
          />
          <TextInput  style={styles.containerInput}
                      keyboardType={'numeric'}
                      placeholder="Treshold oxygen"
                      onChangeText={onChangeOxy}
                      value={oxygen}
          />
          <TextInput  style={styles.containerInput}
                      keyboardType={'numeric'}
                      placeholder="Treshold BPM"
                      onChangeText={onChangeBpm}
                      value={bpm}
          />
          <Button
            title="Send"
            onPress={handleInput}
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
  
export default Config;