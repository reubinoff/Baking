import { Link, useLocation } from "react-router-dom";


function Recipe() {
const { state } = useLocation();
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
