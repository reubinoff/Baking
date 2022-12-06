import React, { useEffect, useMemo } from "react";
import Grid from "@mui/material/Unstable_Grid2"; // Grid version 2

import RecipeCard from "./RecipeCard";
import RecipeCardPlaceholder from "./RecipeCardPlaceholder";
import { useRecipes } from "../data/recipes";
import PlaceholderItems from "./PlaceholderItems";
import Box from "@mui/material/Box";

export default function RecipeGrid() {
  const loader = React.useRef(null);

  const { data, isError, isFetching, fetchNextPage } = useRecipes();

  const handleObserver = React.useCallback(
    (entities) => {
      const target = entities[0];
      if (target.isIntersecting) {
        fetchNextPage();
      }
    },
    [fetchNextPage]
  );

  useEffect(() => {
    const option = {
      root: null,
      rootMargin: "20px",
      threshold: 0,
    };
    const observer = new IntersectionObserver(handleObserver, option);
    if (loader.current) {
      observer.observe(loader.current);
    }
  }, [handleObserver]);

  const recipes = useMemo(
    () =>
      data?.pages.reduce((prev, page) => {
        return {
          info: page.info,
          items: [...prev.items, ...page.items],
        };
      }),
    [data]
  );

  const isRecipesReady = useMemo(() => {
    return !isFetching && recipes?.items.length > 0;
  }, [isFetching, recipes]);

  return (
    <Box sx={{ flexGrow: 1 }}>
      {isError && <div>ERROR</div>}
      <PlaceholderItems
        placeholder={RecipeCardPlaceholder}
        ready={isRecipesReady}
      ></PlaceholderItems>
      <Grid container spacing={2}>
        {recipes?.items.map((recipe) => (
          <Grid xs={12} md={4} key={recipe.id}>
            <RecipeCard recipe={recipe} />
          </Grid>
        ))}
      </Grid>
      <div ref={loader} />
      <div>{isFetching ? "Fetching..." : null}</div>
    </Box>
  );
}
