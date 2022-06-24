import Constants from "expo-constants";

const { manifest } = Constants;

const apiUrl =
  typeof manifest?.packagerOpts === `object` && manifest.packagerOpts.dev
    ? `http://${manifest?.debuggerHost?.split(`:`).shift()?.concat(`:6004`)}`
    : "http://127.0.0.1:6004";

export const API_URL = apiUrl;
export const ID_FALLBACK = -1;
