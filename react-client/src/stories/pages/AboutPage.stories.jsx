import About from '../../pages/About';
import { BrowserRouter as Router } from 'react-router-dom';

const _AboutStory = {
    title: 'Pages/About',
    component: About,
    decorators: [(Story) => <Router><Story /></Router>],

};

export const AboutStory = {
    args: {
       
    },
};
export default _AboutStory;