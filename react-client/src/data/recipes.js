import { UseInfinateScroll } from "./common";

export function useRecipes(page, itemsPerPage=10) {
  const a =  UseInfinateScroll(
    ["Recipes"],
    `/recipe?page=${page}&itemsPerPage=${itemsPerPage}`
  );
  return a;
}