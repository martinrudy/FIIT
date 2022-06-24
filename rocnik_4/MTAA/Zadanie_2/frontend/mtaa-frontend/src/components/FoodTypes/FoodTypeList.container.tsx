import { useQuery } from "react-query";
import { QUERY_KEYS } from "../../api/api";
import Spinner from "../common/Spinner";
import Error from "../common/Error";
import { getFoodTypes } from "../../api/foodType";
import FoodTypeList from "./FoodTypeList";
import { getIngredients } from "../../api/recipe";
import { FC, useState } from "react";
import { useRefrigeratorInUse } from "../../hooks/useRefrigeratorInUse";
import { ID_FALLBACK } from "../../constants/Constants";

type Props = {
  searchQuery: string | undefined;
};

const FoodTypeListContainer: FC<Props> = ({ searchQuery }) => {
  const [isRefreshing, setIsRefreshing] = useState(false);

  const refrigeratorInUse = useRefrigeratorInUse();

  const foodQuery = useQuery(
    [QUERY_KEYS.food, refrigeratorInUse.id],
    getIngredients(refrigeratorInUse.id || ID_FALLBACK),
    {
      enabled: !!refrigeratorInUse,
    }
  );
  const foodTypesQuery = useQuery(
    [QUERY_KEYS.foodTypes, refrigeratorInUse.id],
    getFoodTypes,
    {
      enabled: !!foodQuery.data,
    }
  );

  const onRefresh = async () => {
    setIsRefreshing(true);
    await refrigeratorInUse.refetch();
    await foodQuery.refetch();
    await foodTypesQuery.refetch();
    setIsRefreshing(false);
  };

  if (
    refrigeratorInUse.isLoading ||
    refrigeratorInUse.isIdle ||
    foodTypesQuery.isLoading ||
    foodTypesQuery.isIdle ||
    foodQuery.isLoading ||
    foodQuery.isIdle
  ) {
    return <Spinner />;
  }

  if (
    refrigeratorInUse.isError ||
    foodTypesQuery.isError ||
    foodQuery.isError
  ) {
    return <Error />;
  }

  const fiteredFoodTypes1 = foodTypesQuery.data.filter((foodType) => {
    return !foodQuery.data?.find((food) => food.foodType_id === foodType.id);
  });

  const fiteredFoodTypes = searchQuery
    ? fiteredFoodTypes1.filter((foodType) => {
        return foodType.title.includes(searchQuery);
      })
    : fiteredFoodTypes1;

  return (
    <FoodTypeList
      foodTypes={fiteredFoodTypes}
      refrigeratorId={refrigeratorInUse.id ?? ID_FALLBACK}
      isRefreshing={isRefreshing}
      onRefresh={onRefresh}
    />
  );
};

export default FoodTypeListContainer;
