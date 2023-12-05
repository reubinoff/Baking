import { BrowserRouter as Router } from 'react-router-dom';
import RecipeCard from '../components/RecipeCard';

//👇 This default export determines where your story goes in the story list
export default {
    title: 'Components/RecipeCard',
    component: RecipeCard,
    decorators: [(Story) => <Router><Story /></Router>],
    tags: ['autodocs'],
};

export const RecipeCardStory = {
    args: {
        recipe: {
            id: 1,
            name: 'Test Recipe',
            description: 'Test Description',
            sourdough: true,
            hydration: 100,
            cdn_url: 'https://www.wfp.org/sites/default/files/styles/impact_image/public/images/WFP-food-safety-and-quality.jpg?itok=BA3-FX7c',
            user_id: 1,
        }
    },
};

