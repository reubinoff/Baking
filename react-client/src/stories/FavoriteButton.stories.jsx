import FavoriteRecipeButton from '../components/recipeComponents/FavoriteRecipeButton';

//👇 This default export determines where your story goes in the story list
const _FavoriteRecipeButtonStory = {
    title: 'Components/FavoriteRecipeButton',
    component: FavoriteRecipeButton,
};

export const FavoriteRecipeButtonStory = {
    args: {
        favoirite: false,
    },
};

export default _FavoriteRecipeButtonStory;