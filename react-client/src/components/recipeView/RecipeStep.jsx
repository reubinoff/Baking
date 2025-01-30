import { PropTypes } from "prop-types";
import { Box } from "@mui/material";
import { Typography } from "@mui/material";
import { Grid } from '@mui/system';
import RecipeTimeline from "../recipeComponents/RecipeTimeline";
import moment from "moment";

export default function RecipeStep(props) {
  const {step} = props;
  const currentTimestamp = new moment();
  const timeline = {
    val: currentTimestamp
      .add(props.step.duration_in_seconds, "seconds")
      .format("HH:mm"),
    main: false,
    connector: true,
  };
  return (
    <Box sx={{ flexGrow: 1, mt: "5px" }} key={step.id} {...props}>
      <Grid container spacing={2}>
        <Grid xs={10}>
          <Box>
            <Typography variant="subtitle1">{step.name}</Typography>
            <Typography variant="body1">{step.description}</Typography>
          </Box>
        </Grid>
        <Grid xs={2}>
          <Box display={"flex"} justifyContent={"flex-end"}>
            <RecipeTimeline item={timeline} />
          </Box>
        </Grid>
      </Grid>
    </Box>
  );
}

RecipeStep.propTypes = {
  step: PropTypes.object.isRequired,
};
