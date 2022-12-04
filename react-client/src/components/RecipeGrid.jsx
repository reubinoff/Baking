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
    isFetchingNextPage,
    fetchNextPage,
    hasNextPage,
  } = useRecipes();

  const handleObserver = React.useCallback(
    (entities) => {
      const target = entities[0];
      if (target.isIntersecting) {
        if (hasNextPage && !isFetchingNextPage) {
          fetchNextPage();
        }
      }
    },
    [hasNextPage, isFetchingNextPage, fetchNextPage]
  );

  useEffect(() => {
    const option = {
      root: null,
      rootMargin: "20px",
      threshold: 0,
    };
    const observer = new IntersectionObserver(handleObserver, option);
    if (loader.current && !isFetchingNextPage) observer.observe(loader.current);
  }, [handleObserver, isFetchingNextPage]);

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

  return (
    <div>
      {isError && <div>ERROR</div>}
      <PlaceholderItems
        placeholder={RecipeCardPlaceholder}
        total={1}
        ready={data!==undefined}
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
