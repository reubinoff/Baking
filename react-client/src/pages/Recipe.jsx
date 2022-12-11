import { Link, useLocation } from "react-router-dom";


function Recipe() {
const { state } = useLocation();
  return (
    <div>
      <h2>Favorites!</h2>
      <div>
        <h3>{state}</h3>
      </div>
      <p>
        <Link to="/">Go to the home page</Link>
      </p>
    </div>
  );
}

export default Recipe;
