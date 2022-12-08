import "./App.css";
import RecipeGrid from "./components/RecipeGrid";
import { Box } from "@mui/material";
import BakingNavBar from "./components/BakingNavBar";
import Toolbar from "@mui/material/Toolbar";


function App() {

  return (
    <Box sx={{ display: "flex" }}>
      <BakingNavBar></BakingNavBar>
      <Box component="main" sx={{ pt: 9, pr: 2, pl: 2, width: 1 }}>
        <RecipeGrid />
      </Box>
    </Box>
  );
}

export default App;
