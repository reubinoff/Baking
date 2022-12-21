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
   const [requiredValues, setRequiredValues] = React.useState();

  React.useEffect(() => {
    if (isFetching === false && isFetched === true) {
      setRecipe({ ...data });
      setRequiredValues({
        reqTotalLoafWeight: 700,
        reqTotalLoafCount: 1,
        reqHyration: data.hydration,
      });
    }
  }, [isFetching, data, isFetched]);


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
       { requiredValues!== undefined? <RecipeQuantitySelector
          requiredValues={requiredValues}
          setRequiredValues={setRequiredValues}
        /> : null}
        <Box>
          {GetRecipeView(isFetched, recipe, requiredValues)}
          {error && <div>Error: {error.message}</div>}
        </Box>
      </Box>
    </Box>
  );
}

function GetRecipeView(isFetched, recipe, requiredValues) {
  if (isFetched === true && recipe !== undefined) {
    return (
      <RecipeView
        recipe={recipe}
        reqHyration={requiredValues.reqHyration}
        reqTotalLoafWeight={requiredValues.reqTotalLoafWeight}
        reqTotalLoafCount={requiredValues.reqTotalLoafCount}
      />
    );
  }
}

export default Recipe;
