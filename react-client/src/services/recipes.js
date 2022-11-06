import { get } from "./api";

export const getRecipes = (page = 1, itemsPerPage = 10) => {
  return get(`recipe?page=${page}&itemsPerPage=${itemsPerPage}`);
};
