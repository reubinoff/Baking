import * as recipesTypes from "../actions/recipesActions";
import * as recipeTypes from "../actions/recipeActions";
// Initial state
const initialState = {
  recipes: [],
};

// Reducer function
const recipeReducer = (state = initialState, action) => {
  switch (action.type) {
    case recipeTypes.ADD_RECIPE:
      return {
        ...state,
        recipes: [...state.recipes, action.payload],
      };
    case recipeTypes.DELETE_RECIPE:
      return {
        ...state,
        recipes: state.recipes.filter((recipe) => recipe.id !== action.payload),
      };
    case recipeTypes.UPDATE_RECIPE:
      return {
        ...state,
        recipes: state.recipes.map((recipe) =>
          recipe.id === action.payload.recipeId
            ? action.payload.updatedRecipe
            : recipe
        ),
      };
    case recipeTypes.GET_RECIPE:
      return {
        ...state,
        recipes: state.recipes.find((recipe) => recipe.id === action.payload),
      };
    case recipesTypes.GET_RECIPES:
      return {
        ...state,
        recipes: action.payload,
      };
    default:
      return state;
  }
};

export default recipeReducer;
