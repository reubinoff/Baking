import { PropTypes } from "prop-types";
import { Box } from "@mui/material";
import { Typography } from "@mui/material";
import RecipeStep from "./RecipeStep";
import RecipeTimeline from "../recipeComponents/RecipeTimeline";
import { Grid } from '@mui/system';
export default function RecipeProcedure(props) {
  const { steps } = props.procedure;
  const { startTimestamp } = props;

  return (
    <Box display={"flex"} flexDirection={"column"}>
      <Grid container spacing={0}>
        <Grid xs={9}>
          <Typography variant="h6">{props.procedure.name}</Typography>
          <Typography variant="body1">{props.procedure.description}</Typography>
        </Grid>
        <Grid xs={3}>
          <RecipeTimeline item={generateItem(startTimestamp)} />
        </Grid>
      </Grid>
      {steps.map((step) => (
        <RecipeStep step={step} key={step.id} />
      ))}
    </Box>
  );
}

function generateItem(startTimestamp) {
  return {
    val: startTimestamp.format("HH:mm"),
    main: false,
    connector: true,
  };
}

RecipeProcedure.propTypes = {
  procedure: PropTypes.object.isRequired,
  startTimestamp: PropTypes.object.isRequired,
};
