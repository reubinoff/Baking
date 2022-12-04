import React, { useEffect, useMemo } from "react";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import RecipeCard from "./RecipeCard";
import RecipeCardPlaceholder from "./RecipeCardPlaceholder";
import { useRecipes } from "../data/recipes";
import PlaceholderItems from "./PlaceholderItems";

export default function RecipeGrid() {
  const loader = React.useRef(null);

  const {
    data,
    isError,
    isFetching,
    fetchNextPage,
  } = useRecipes();

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
    if (loader.current ) {
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
    <div>
      {isError && <div>ERROR</div>}
      <PlaceholderItems
        placeholder={RecipeCardPlaceholder}
        ready={isRecipesReady}
      ></PlaceholderItems>
      <Row xs={1} md={2} lg={3} className="g-4">
        {recipes?.items.map((recipe) => (
          <Col key={recipe.id}>
            <RecipeCard recipe={recipe} />
          </Col>
        ))}
      </Row>
      <div ref={loader} />
      <div>{isFetching ? "Fetching..." : null}</div>
    </div>
  );
}

