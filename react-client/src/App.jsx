import "./App.css";
import { Route, Routes } from "react-router-dom";
import HomePage from "./pages/HomePage";
import Layout from "./pages/Layout";
import About from "./pages/About";
import Settings from "./pages/Settings";
import Favorites from "./pages/Favorites";
import Recipe from "./pages/Recipe";
import ErrorPage from "./pages/ErrorPage";



function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout/>}>
        <Route index element={<HomePage />} />
        <Route path="about" element={<About />} />
        <Route path="settings" element={<Settings />} />
        <Route path="favorites" element={<Favorites />} />
        <Route path="recipe/:recipeId" element={<Recipe />} />
        <Route path="*" element={<ErrorPage />} />
      </Route>
    </Routes>
  );
}

export default App;
