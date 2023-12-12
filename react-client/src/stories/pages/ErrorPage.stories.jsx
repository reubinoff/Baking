import ErrorPage from '../../pages/ErrorPage';
import { BrowserRouter as Router } from 'react-router-dom';

const _ErrorPageStory = {
    title: 'Pages/ErrorPage',
    component: ErrorPage,
    decorators: [(Story) => <Router><Story /></Router>],

};

export const ErrorPageStory = {
    args: {
       
    },
};

export default _ErrorPageStory;
