import { Link, useLocation } from "react-router-dom";
import _ from "lodash";


function Recipe() {
const { state } = useLocation();
    if ( _.isUndefined( state?.recipe)) {
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
    <div>
      <h2>{state.recipe.name}</h2>
      <div>
        <p>{state.recipe.description}</p>
      </div>
      <p>
        <Link to="/">Go to the home page</Link>
      </p>
    </div>
  );
}

export default Recipe;
