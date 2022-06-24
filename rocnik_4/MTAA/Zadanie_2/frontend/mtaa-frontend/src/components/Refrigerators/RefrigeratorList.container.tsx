import { useQuery } from "react-query";
import { QUERY_KEYS } from "../../api/api";
import Spinner from "../common/Spinner";
import Error from "../common/Error";
import RefrigeratorList from "./RefrigeratorList";
import { getRefrigerators } from "../../api/refrigerator";
import { useUserInfo } from "../../contexts/UserInfoContext";
import { ID_FALLBACK } from "../../constants/Constants";
import { useState } from "react";

const RefrigeratorListContainer = () => {
  const [isRefreshing, setIsRefreshing] = useState(false);

  const { userId } = useUserInfo();

  const refrigeratorsQuery = useQuery(
    [QUERY_KEYS.refrigerators, userId],
    getRefrigerators(userId ?? ID_FALLBACK)
  );

  const onRefresh = async () => {
    setIsRefreshing(true);
    await refrigeratorsQuery.refetch();
    setIsRefreshing(false);
  };

  if (refrigeratorsQuery.isLoading || refrigeratorsQuery.isIdle) {
    return <Spinner />;
  }

  if (refrigeratorsQuery.isError) {
    return <Error />;
  }

  return (
    <RefrigeratorList
      refrigerators={refrigeratorsQuery.data}
      isRefreshing={isRefreshing}
      onRefresh={onRefresh}
    />
  );
};

export default RefrigeratorListContainer;
