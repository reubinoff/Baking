

import { Link } from "react-router-dom";

function About() {
  return (
    <div>
      <h2>About!</h2>
      <p>
        <Link to="/">Go to the home page</Link>
      </p>
    </div>
  );
}

export default About;