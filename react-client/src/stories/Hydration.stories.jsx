import Hydration from '../components/recipeComponents/Hydration';

//👇 This default export determines where your story goes in the story list
const HydrationStoryComponent =  {
    title: 'Components/Hydration',
    component: Hydration,
};

export const HydrationStory = {
    args: {
        hydration: 100,
    },
};

export default HydrationStoryComponent;