import HomePage from '../../pages/HomePage';
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

const _HomePageStory = {
    title: 'Pages/HomePage',
    component: HomePage,
    decorators: [(Story) =>
        <QueryClientProvider client={queryClient}>
            <Router><Story /></Router>
        </QueryClientProvider>],

};

export const HomePageStory = {
    args: {

    },
};

export default _HomePageStory;
