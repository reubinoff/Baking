import React, { useEffect } from "react";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import RecipeCard from "./RecipeCard";
import RecipeCardPlaceholder from "./RecipeCardPlaceholder";
import { useRecipes } from "../data/recipes";

export default function RecipeGrid() {
  const [page, setPage] = React.useState(1);
  const loader = React.useRef(null);

  const {
    status,
    data,
    isError,
    isFetching,
    isFetchingNextPage,
    fetchNextPage,
    hasNextPage,
  } = useRecipes(page);

  const handleObserver = React.useCallback((entities) => {
    const target = entities[0];
    if (target.isIntersecting) {
      // setPage((prev) => prev + 1);
      fetchNextPage();
    }
  }, []);

  useEffect(() => {
    const option = {
      root: null,
      rootMargin: "20px",
      threshold: 0,
    };
    const observer = new IntersectionObserver(handleObserver, option);
    if (loader.current) observer.observe(loader.current);
  }, [handleObserver]);

  return (
    <div>
      {isError && <div>ERROR</div>}
      <Row xs={1} md={2} lg={3} className="g-4">
        {isFetching &&
          [1, 2, 3, 4, 5, 6, 7, 8, 9].map((i) => (
            <Col key={i}>
              <RecipeCardPlaceholder />
            </Col>
          ))}
        {!isFetching &&
          data.pages.map((group, i) => (
            <React.Fragment key={i}>
              {data.items.map((recipe) => (
                <Col key={recipe.id}>
                  <RecipeCard recipe={recipe} />
                </Col>
              ))}
            </React.Fragment>
          ))}
      </Row>
      <div ref={loader} />
    </div>
  );
}

//   // featch data
//   componentDidMount() {
//     this.setState({ loading: true });
//     getRecipes(1, 10).then((data) =>
//       this.setState({ recipes: data.items, loading: false })
//     );
//   }

//   render() {
//     const { loading, recipes } = this.state;

//     if (loading) {
//       return (
//         <div>
//           <Row xs={1} md={2} lg={4} className="g-4">
//             {[...Array(10).keys()].map((i) => (
//               <Col key={i}>
//                 <RecipeCardPlaceholder />
//               </Col>
//             ))}
//           </Row>
//         </div>
//       );
//     } else {
//       return (
//         <div>
//           <Row xs={1} md={2} lg={4} className="g-4">
//             {recipes.map((recipe) => (
//               <Col key={recipe.id}>
//                 <RecipeCard recipe={recipe} />
//               </Col>
//             ))}
//           </Row>
//         </div>
//       );
//     }
//   }
// }

// export default RecipeGrid;
