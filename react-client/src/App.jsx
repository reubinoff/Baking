import "./App.css";
import { Box } from "@mui/material";
import BakingNavBar from "./components/BakingNavBar";
import { Route, Routes, Outlet } from "react-router-dom";
import Home from "./pages/Home";
import About from "./pages/About";
import Settings from "./pages/Settings";
import Favorites from "./pages/Favorites";
import Recipe from "./pages/Recipe";
import ErrorPage from "./pages/ErrorPage";


function Layout() {
  return (
    <Box sx={{ display: "flex" }}>
      <BakingNavBar setQuery={() => console.log("")}></BakingNavBar>
      <Box component="main" sx={{ pt: 9, pr: 2, pl: 2, width: 1 }}>
        <Outlet />
      </Box>
    </Box>
  );
}

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Home />} />
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
