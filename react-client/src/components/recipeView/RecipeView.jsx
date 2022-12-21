import { PropTypes } from "prop-types";

import { Box } from "@mui/material";
import { Paper } from "@mui/material";
import Typography from "@mui/material/Typography";
import RecipeIngridients from "./RecipeIngridients";
import RecipeProcedure from "./RecipeProcedure";
// import Hydration from "../recipeComponents/Hydration";
import Grid from "@mui/material/Unstable_Grid2"; // Grid version 2
// import ScaleIcon from '@mui/icons-material/Scale';
export default function RecipeView(props) {
  const { recipe } = props;
  return (
    <Box>
      <Grid container spacing={2}>
        <Grid xs={9}>
          <h1>{recipe.name}</h1>
          <p>{recipe.description}</p>
        </Grid>
        {/* <Grid xs={3}>
          <Hydration
            hydration={recipe.hydration}
            sx={{ position: "relative", top: "30%", left: "30%" }}
          />
          <ScaleIcon/>
        </Grid> */}
      </Grid>

      <Paper>
        <Typography variant="h6">
          Ingredients
          <RecipeIngridients
            ingredients={recipe.ingredients}
            currentHyration={recipe.hydration}
            reqTotalLoafWeight={props.reqTotalLoafWeight}
            reqHyration={props.reqHyration}
            reqTotalLoafCount={props.reqTotalLoafCount}
          />
        </Typography>
      </Paper>

      <Paper sx={{ mt: 5 }}>
        <Typography variant="h6">
          Procedures
          {recipe.procedures.map((procedure) => (
            <RecipeProcedure key={procedure.name} procedure={procedure} />
          ))}
        </Typography>
      </Paper>
    </Box>
  );
}

RecipeView.propTypes = {
  recipe: PropTypes.object.isRequired,
  reqHyration: PropTypes.number.isRequired, // undefined for same as recipe
  reqTotalLoafWeight: PropTypes.number.isRequired, // undefined for same as recipe
  reqTotalLoafCount: PropTypes.number.isRequired, // undefined for same as recipe
};
