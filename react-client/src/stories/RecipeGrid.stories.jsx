import RecipeGrid from '../components/RecipeGrid';
import { BrowserRouter as Router } from 'react-router-dom';
import { QueryClient } from 'react-query';
import { QueryClientProvider } from 'react-query';

const queryClient = new QueryClient({
    defaultOptions: {
        queries: {
            refetchOnWindowFocus: false,
            cacheTime: 600000, // 10 mins
        },
    },
});

const _RecipeGridStory = {
    title: 'Components/RecipeGrid',
    component: RecipeGrid,
    decorators: [(Story) =>
        <QueryClientProvider client={queryClient} >
            <Router><Story /></Router>
        </QueryClientProvider >],

};

export const RecipeGridStory = {
    args: {
        query: '',
    },
};

export default _RecipeGridStory;