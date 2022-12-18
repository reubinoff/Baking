import { UseInfinateScroll, useFetch } from "./common";
import handleError from "../utils/handleError";

const BASE_URL = process.env.REACT_APP_BASE_URL;

export function useRecipes(query, itemsPerPage = 10) {
  const queryMethod = async ({ pageParam = 1 }) => {
    let path = `${BASE_URL}/recipe?page=${pageParam}&itemsPerPage=${itemsPerPage}`;
    if (query && query.length > 0) {
      path += `&q=${query}`;
    }

    return await fetch(path).then(handleError);
  };

  return UseInfinateScroll(["Recipes", query], queryMethod);
}

export function useRecipe(id) {

  let path = `recipe/${id}`;

  return useFetch(["Recipe", id], path);
}