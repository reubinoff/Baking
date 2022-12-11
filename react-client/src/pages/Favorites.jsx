import { Link } from "react-router-dom";

function Favorites() {
  return (
    <div>
      <h2>Favorites!</h2>
      <p>
        <Link to="/">Go to the home page</Link>
      </p>
    </div>
  );
}

export default Favorites;
