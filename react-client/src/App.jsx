import "./App.css";
import { Box } from "@mui/material";
import BakingNavBar from "./components/BakingNavBar";
import { Route, Routes, Outlet } from "react-router-dom";
import { Favorites, About, ErrorPage, Home, Settings, Recipe } from "./pages";

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
