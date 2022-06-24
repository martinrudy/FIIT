import { RTCView } from "react-native-webrtc";
import { StyleSheet, View } from "react-native";
import { RootTabScreenProps, RouteNames } from "../types/TNavigation";
import { useState } from "react";
import WebRTC from "../utils/webRTCUtils";
import Button from "../components/common/Button";

const VideoCallScreen = ({
  navigation,
}: RootTabScreenProps<RouteNames.Recipes>) => {
  const [remoteStreamURL, setRemoteStreamURL] = useState();
  const [webrtc, setWebrtc] = useState<WebRTC>();
  const NewWebRTC: any = RTCView;

  const onConnect = () => {
    const webrtcInstance = webrtc ?? new WebRTC();
    webrtcInstance.onRemoteStreamObtained = (stream: any) => {
      setRemoteStreamURL(stream.toURL());
    };
    webrtcInstance.connect();
    setWebrtc(webrtcInstance);
  };

  const onDisconnect = () => {
    webrtc?.stop();
    setRemoteStreamURL(undefined);
  };

  return (
    <View style={styles.container}>
      <NewWebRTC streamURL={remoteStreamURL} style={styles.webrtcStream} />
      <Button text="Connect" onPress={onConnect} style={styles.connectButton} />
      <Button text="Disconnect" onPress={onDisconnect} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
  },
  webrtcStream: {
    width: "100%",
    height: 300,
    marginBottom: 16,
    alignSelf: "center",
    backgroundColor: "lightgray",
  },
  connectButton: {
    marginBottom: 8,
  },
});

export default VideoCallScreen;
