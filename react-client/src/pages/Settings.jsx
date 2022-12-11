import { Link } from "react-router-dom";

function Settings() {
  return (
    <div>
      <h2>Settings!</h2>
      <p>
        <Link to="/">Go to the home page</Link>
      </p>
    </div>
  );
}

export default Settings;
