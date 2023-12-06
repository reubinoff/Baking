import { BrowserRouter as Router } from 'react-router-dom';
import RecipeCard from '../components/RecipeCard';

//👇 This default export determines where your story goes in the story list
export default {
    title: 'Components/RecipeCard',
    component: RecipeCard,
    decorators: [(Story) => <Router><Story /></Router>],
    argTypes: { onClick: { action: 'button-clicked' } }
};

export const RecipeCardStory = {
    args: {
        recipe: {
            id: 1,
            name: 'Rye Bread',
            description: 'To conditionally render CardMedia based on the loading state while still keeping it in the DOM, you can use CSS for hiding and showing the component.',
            sourdough: true,
            hydration: 100,
            cdn_url: 'https://www.wfp.org/sites/default/files/styles/impact_image/public/images/WFP-food-safety-and-quality.jpg?itok=BA3-FX7c',
            user_id: 1,
        }
    },
};

