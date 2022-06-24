import {
  createContext,
  Dispatch,
  FC,
  SetStateAction,
  useContext,
  useEffect,
  useState,
} from "react";
import {
  getAsyncStorageItem,
  setAsyncStorageItem,
  STORAGE_KEYS,
} from "../utils/storageUtils";

type UserInfoContextType = {
  userId: number | null | undefined;
  setUserId: Dispatch<SetStateAction<number | null | undefined>>;
  isLoading: boolean;
};

const UserInfoContext = createContext<UserInfoContextType | undefined>(
  undefined
);

export const UserInfoProvider: FC = ({ children }) => {
  const [userId, setUserId] = useState<number | null>();
  const [refrigeratorId, setRefrigeratorId] = useState<number>();
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (userId) {
      setAsyncStorageItem(STORAGE_KEYS.USER_ID, userId);
    }
    if (userId || userId === null) {
      setIsLoading(false);
    }
  }, [userId]);

  useEffect(() => {
    if (refrigeratorId)
      setAsyncStorageItem(STORAGE_KEYS.REFRIGERATOR_ID, refrigeratorId);
  }, [userId]);

  useEffect(() => {
    (async () => {
      const userId = await getAsyncStorageItem<number>(STORAGE_KEYS.USER_ID);
      const refrigeratorId = await getAsyncStorageItem<number>(
        STORAGE_KEYS.REFRIGERATOR_ID
      );
      if (userId) setUserId(userId);
      else setUserId(null);
      if (refrigeratorId) setRefrigeratorId(refrigeratorId);
    })();
  }, []);

  return (
    <UserInfoContext.Provider
      value={{
        userId: userId,
        setUserId: setUserId,
        isLoading,
      }}
    >
      {children}
    </UserInfoContext.Provider>
  );
};

export const useUserInfo = () => {
  const context = useContext(UserInfoContext);
  if (context === undefined) {
    throw new Error("useUserInfoContext must be used within UserInfoProvider");
  }
  return context;
};
