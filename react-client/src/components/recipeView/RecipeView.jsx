import { PropTypes } from "prop-types";

import { Box } from "@mui/material";
import { Paper } from "@mui/material";
import Typography from "@mui/material/Typography";
import RecipeIngridients from "./RecipeIngridients";
import RecipeProcedure from "./RecipeProcedure";
import Grid from "@mui/material/Unstable_Grid2"; // Grid version 2
// import RecipeTimeline from "../recipeComponents/RecipeTimeline";
export default function RecipeView(props) {
  const { recipe } = props;
  return (
    <Box>
      <Grid container spacing={2}>
        <Grid xs={9}>
          <Typography variant="h4">{recipe.name}</Typography>
          <Typography variant="body1">{recipe.description}</Typography>
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
        <Typography variant="h5" sx={{ ml: "5px" }}>
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

      <Grid container spacing={2}>
        <Grid xs={12}>
          <Paper sx={{ mt: 5 }}>
            <Typography variant="h5" sx={{ ml: "5px" }}>
              Procedures
              {recipe.procedures.map((procedure) => (
                <Box key={procedure.name} sx={{ mt: "20px" }}>
                  <RecipeProcedure procedure={procedure} />
                </Box>
              ))}
            </Typography>
          </Paper>
        </Grid>
        <Grid >
          {/* <RecipeTimeline /> */}
        </Grid>
      </Grid>
    </Box>
  );
}

RecipeView.propTypes = {
  recipe: PropTypes.object.isRequired,
  reqHyration: PropTypes.number.isRequired, // undefined for same as recipe
  reqTotalLoafWeight: PropTypes.number.isRequired, // undefined for same as recipe
  reqTotalLoafCount: PropTypes.number.isRequired, // undefined for same as recipe
};
