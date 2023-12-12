// Action Types
export const GET_RECIPES = "GET_RECIPES";

// Action Creators
export const getRecipes = (recipeId) => {
  return {
    type: GET_RECIPES,
    payload: recipeId,
  };
};
