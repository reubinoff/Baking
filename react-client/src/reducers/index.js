import { combineReducers } from "redux";
import recipeReducer from "./recipeReducer";

// Combine reducers
const rootReducer = combineReducers({
    recipes: recipeReducer,
});

export default rootReducer;