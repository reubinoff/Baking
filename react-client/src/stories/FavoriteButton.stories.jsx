import FavoriteRecipeButton from '../components/recipeComponents/FavoriteRecipeButton';

//👇 This default export determines where your story goes in the story list
export default {
    title: 'Components/FavoriteRecipeButton',
    component: FavoriteRecipeButton,
    tags: ['autodocs'],
};

export const FavoriteRecipeButtonStory = {
    args: {
        favoirite: false,
    },
};

