import { useQuery } from "react-query";
import { QUERY_KEYS } from "../../api/api";
import { getIngredients } from "../../api/recipe";
import Spinner from "../common/Spinner";
import Error from "../common/Error";
import FoodList from "./FoodList";
import { useState } from "react";
import { useRefrigeratorInUse } from "../../hooks/useRefrigeratorInUse";
import { ID_FALLBACK } from "../../constants/Constants";

const FoodListContainer = () => {
  const [isRefreshing, setIsRefreshing] = useState(false);

  const refrigeratorInUse = useRefrigeratorInUse();
  const foodQuery = useQuery(
    [QUERY_KEYS.food, refrigeratorInUse.id],
    getIngredients(refrigeratorInUse.id ?? ID_FALLBACK),
    {
      enabled: !!refrigeratorInUse,
    }
  );

  const onRefresh = async () => {
    setIsRefreshing(true);
    await foodQuery.refetch();
    setIsRefreshing(false);
  };

  if (
    refrigeratorInUse.isLoading ||
    refrigeratorInUse.isIdle ||
    foodQuery.isLoading ||
    foodQuery.isIdle
  ) {
    return <Spinner />;
  }

  if (refrigeratorInUse.isError || foodQuery.isError) {
    return <Error />;
  }

  return (
    <FoodList
      ingredients={foodQuery.data}
      onRefresh={onRefresh}
      isRefreshing={isRefreshing}
      refrigeratorId={refrigeratorInUse.id ?? ID_FALLBACK}
    />
  );
};

export default FoodListContainer;
