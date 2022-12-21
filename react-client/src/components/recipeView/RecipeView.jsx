import { PropTypes } from "prop-types";

import { Box } from "@mui/material";
import { Paper } from "@mui/material";
import Typography from "@mui/material/Typography";
import RecipeIngridients from "./RecipeIngridients";
import RecipeProcedure from "./RecipeProcedure";
import Grid from "@mui/material/Unstable_Grid2"; // Grid version 2
import moment from "moment";
export default function RecipeView(props) {
  const { recipe } = props;
  var d = new moment();
  const procedures = recipe.procedures.sort((a, b) => {
    return a.order - b.order;
  });
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
      <Box sx={{ mt: 5 }}>
        <Typography variant="h5" sx={{ ml: "5px" }}>
          Procedures
          {procedures.map((procedure, idx) => {
            console.log("idx", idx);
            if (idx > 0) {
              d = d.add(
                procedures[idx - 1].duration_in_seconds,
                "seconds"
              );
            }
            return (
              <Box key={procedure.name} sx={{ mt: "20px" }}>
                {procedure.duration_in_seconds}
                <RecipeProcedure procedure={procedure} startTimestamp={d} />
              </Box>
            );
          })}
        </Typography>
      </Box>
    </Box>
  );
}

RecipeView.propTypes = {
  recipe: PropTypes.object.isRequired,
  reqHyration: PropTypes.number.isRequired, // undefined for same as recipe
  reqTotalLoafWeight: PropTypes.number.isRequired, // undefined for same as recipe
  reqTotalLoafCount: PropTypes.number.isRequired, // undefined for same as recipe
};
