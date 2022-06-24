import { useQuery } from "react-query";
import { QUERY_KEYS } from "../api/api";
import { getRefrigerators } from "../api/refrigerator";
import { ID_FALLBACK } from "../constants/Constants";
import { useUserInfo } from "../contexts/UserInfoContext";

const useRefrigeratorInUse = () => {
  const { userId } = useUserInfo();
  const refrigeratorsQuery = useQuery(
    [QUERY_KEYS.refrigerators, userId],
    getRefrigerators(userId ?? ID_FALLBACK)
  );

  const id = refrigeratorsQuery.data?.find((r) => r.in_use)?.id;

  return { id, ...refrigeratorsQuery };
};

export { useRefrigeratorInUse };
