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
      hydration: index,
      cdn_url: "https://images.baking.reubinoff.com/0619d8f4-a288-47b9-b892-995e726c7b2c.jpeg"
    });
  }
  return <RecipeGrid recipes={recipes} />;
}

export default App;
