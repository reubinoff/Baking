// Action Types
export const ADD_RECIPE = 'ADD_RECIPE';
export const DELETE_RECIPE = 'DELETE_RECIPE';
export const UPDATE_RECIPE = 'UPDATE_RECIPE';
export const GET_RECIPE = 'GET_RECIPE';

// Action Creators
export const addRecipe = (recipe) => ({
    type: ADD_RECIPE,
    payload: recipe,
});

export const deleteRecipe = (recipeId) => ({
    type: DELETE_RECIPE,
    payload: recipeId,
});

export const updateRecipe = (recipeId, updatedRecipe) => ({
    type: UPDATE_RECIPE,
    payload: {
        recipeId,
        updatedRecipe,
    },
});

export const getRecipe = (recipeId) => ({
    type: GET_RECIPE,
    payload: recipeId,
});