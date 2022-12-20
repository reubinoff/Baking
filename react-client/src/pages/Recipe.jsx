import React from "react";
import { useParams } from "react-router-dom";
import RecipeView from "../components/recipeView/RecipeView";
import { useRecipe } from "../data/recipes";
import { Box } from "@mui/material";
import RecipeQuantitySelector from "../components/recipeView/RecipeQuantitySelector";
import CircularProgress from "@mui/material/CircularProgress";


function Recipe() {
  const { recipeId } = useParams();
  const { data, isFetching, error, isFetched } = useRecipe(recipeId);

  const [recipe, setRecipe] = React.useState();

  React.useEffect(() => {
    if (isFetching === false && isFetched === true) {
      setRecipe({ ...data });
    }
  }, [isFetching, data, isFetched]);
   const [requiredValues, setRequiredValues] = React.useState({
     reqHyration: 70,
     reqTotalLoafWeight: 1000,
     reqTotalLoafCount: 1,
   });


  return (
    // Loader
    <Box>
      <CircularProgress 
        sx={{
          position: "absolute",
          top: "50%",
          left: "50%",
          transform: "translate(-50%, -50%)",
          display: isFetching === true ? "flex" : "none",
        }}
      />

      <Box sx={{ display: isFetching === true ? "none" : "block" }}>
        <RecipeQuantitySelector
          requiredValues={requiredValues}
          setRequiredValues={setRequiredValues}
        />
        <Box>
          {recipe === undefined ? (
            <div>Loading...</div>
          ) : (
            <RecipeView
              recipe={recipe}
              reqHyration={requiredValues.reqHyration}
              reqTotalLoafWeight={requiredValues.reqTotalLoafWeight}
              reqTotalLoafCount={requiredValues.reqTotalLoafCount}
            />
          )}
          {error && <div>Error: {error.message}</div>}
        </Box>
      </Box>
    </Box>
  );
}

export default Recipe;
