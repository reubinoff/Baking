import { Link, useLocation } from "react-router-dom";
import RecipeView from "../components/recipeView/RecipeView";

import _ from "lodash";

function Recipe() {
  const { state } = useLocation();

  if (_.isUndefined(state?.recipe)) {
    return (
      <div>
        <h2>Recipe not found</h2>
        <p>
          <Link to="/">Go to the home page</Link>
        </p>
      </div>
    );
  }
  return (
    <RecipeView recipe={state.recipe} >
      
    </RecipeView>

  );
}

export default Recipe;
