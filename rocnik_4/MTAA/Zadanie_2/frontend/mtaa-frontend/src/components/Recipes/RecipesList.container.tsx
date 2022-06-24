import { useQuery } from "react-query";
import { QUERY_KEYS } from "../../api/api";
import { getRecipes } from "../../api/recipe";
import Spinner from "../common/Spinner";
import Error from "../common/Error";
import RecipeList from "./RecipeList";
import { ID_FALLBACK } from "../../constants/Constants";
import { useRefrigeratorInUse } from "../../hooks/useRefrigeratorInUse";
import { useState } from "react";

const RecipesListContainer = () => {
  const [isRefreshing, setIsRefreshing] = useState(false);
  const refrigeratorInUse = useRefrigeratorInUse();

  const recipesQuery = useQuery(
    [QUERY_KEYS.recipes, refrigeratorInUse.id],
    getRecipes(refrigeratorInUse.id ?? ID_FALLBACK),
    {
      enabled: !!refrigeratorInUse.id,
    }
  );

  const onRefresh = async () => {
    setIsRefreshing(true);
    await recipesQuery.refetch();
    setIsRefreshing(false);
  };

  if (
    refrigeratorInUse.isLoading ||
    refrigeratorInUse.isIdle ||
    recipesQuery.isLoading ||
    recipesQuery.isIdle
  ) {
    return <Spinner />;
  }

  if (refrigeratorInUse.isError || recipesQuery.isError) {
    return <Error />;
  }

  return (
    <RecipeList
      recipes={recipesQuery.data}
      isRefreshing={isRefreshing}
      onRefresh={onRefresh}
    />
  );
};

export default RecipesListContainer;
