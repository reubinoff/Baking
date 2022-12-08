import React, { useEffect, useMemo } from "react";
import Grid from "@mui/material/Unstable_Grid2"; // Grid version 2

import RecipeCard from "./RecipeCard";
import RecipeCardPlaceholder from "./RecipeCardPlaceholder";
import { useRecipes } from "../data/recipes";
import Box from "@mui/material/Box";

import Fab from "@mui/material/Fab";
import KeyboardArrowUpIcon from "@mui/icons-material/KeyboardArrowUp";
import ScrollTop from "./ScrollTop";


export default function RecipeGrid(props) {
  const loader = React.useRef(null);
  const itemsPerPage = 10;

  const { data, isError, isFetching, fetchNextPage } = useRecipes(itemsPerPage);

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
    if (recipes?.items.length > 0) {
      return true;
    }
    return !isFetching;
  }, [isFetching, recipes]);

  return (
    <Box sx={{ flexGrow: 1 }}>
      <div id="back-to-top-anchor" />
      {isError && <div>ERROR</div>}
      <Grid container spacing={2}>
        { GetSkelaton(itemsPerPage, isRecipesReady)}
        {isRecipesReady &&
          recipes?.items.map((recipe) => (
            <Grid xs={12} sm={6} md={3} key={recipe.id}>
              <RecipeCard recipe={recipe} />
            </Grid>
          ))}
      </Grid>
      <ScrollTop {...props}>
        <Fab size="small" aria-label="scroll back to top">
          <KeyboardArrowUpIcon />
        </Fab>
      </ScrollTop>
      <div ref={loader} />
      <div>{isFetching ? "Fetching..." : null}</div>
    </Box>
  );
}

function GetSkelaton(itemsPerPage, toShow) {
  return (
    <React.Fragment>
      {!toShow &&
        Array.from(Array(itemsPerPage)).map((_, index) => (
          <Grid xs={12} sm={6} md={3} key={index}>
            <RecipeCardPlaceholder />
          </Grid>
        ))}
    </React.Fragment>
  );
}

