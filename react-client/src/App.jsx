import "./App.css";
import RecipeGrid from "./components/RecipeGrid";
import { Box } from "@mui/material";
import BakingNavBar from "./components/BakingNavBar";

function App() {

  return (
    <Box sx={{ display: "flex" }}>
      <BakingNavBar></BakingNavBar>
      <RecipeGrid />
    </Box>
  );
}

export default App;
