import "./App.css";
import React from "react";
import RecipeGrid from "./components/RecipeGrid";
import "bootstrap/dist/css/bootstrap.min.css";

function App() {
  let recipes = [];
  for (let index = 0; index < 10; index++) {
    recipes.push({
      id: index,
      name: "Bread",
      description: "A delicious loaf of bread",
    });
  }
  return <RecipeGrid recipes={recipes} />;
}

export default App;
