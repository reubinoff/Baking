import React from "react";
import { get } from "./api";

export const getRecipes = (page = 1, itemsPerPage = 10) => {
  const [recipes, setRecipes] = React.useState([]);
  const { loading, error, data } = get(
    `recipe?page=${page}&itemsPerPage=${itemsPerPage}`
  );
  if (!loading) {
    setRecipes((prev) => [...prev, data.items]);
    return { loading, error, recipes };
  }
  
};
