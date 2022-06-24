import AsyncStorage from "@react-native-async-storage/async-storage";

export enum STORAGE_KEYS {
  USER_ID = "@user_id",
  REFRIGERATOR_ID = "@refrigerator_id",
}

export const setAsyncStorageItem = async <T>(
  key: STORAGE_KEYS,
  value: T
): Promise<void> => {
  try {
    const json = JSON.stringify(value);
    await AsyncStorage.setItem(key, json);
  } catch (e) {
    console.error(e);
  }
};

export const getAsyncStorageItem = async <T>(
  key: STORAGE_KEYS
): Promise<T | null> => {
  try {
    const json = await AsyncStorage.getItem(key);
    return json === null ? null : JSON.parse(json);
  } catch (e) {
    console.error(e);
  }
  return null;
};
