import "./App.css";
import React from "react";
import RecipeGrid from "./components/RecipeGrid";
import { Box } from "@mui/material";
import BakingNavBar from "./components/BakingNavBar";

function App() {
  const [query, setQuery] = React.useState("")
  return (
    <Box sx={{ display: "flex" }}>
      <BakingNavBar setQuery={setQuery}></BakingNavBar>
      <Box component="main" sx={{ pt: 9, pr: 2, pl: 2, width: 1 }}>
        <RecipeGrid query={query} />
      </Box>
    </Box>
  );
}

export default App;
