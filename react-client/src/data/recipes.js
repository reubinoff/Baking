import { UseInfinateScroll } from "./common";
import handleError from "../utils/handleError";

const BASE_URL = process.env.REACT_APP_BASE_URL;

export function useRecipes(itemsPerPage = 10) {
  const queryMethod = async ({ pageParam = 1 }) => {
    const path = `${BASE_URL}/recipe?page=${pageParam}&itemsPerPage=${itemsPerPage}`;

    return await fetch(path).then(handleError);
  };

  return UseInfinateScroll(["Recipes"], queryMethod);
}