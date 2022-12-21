import React from 'react';
import { PropTypes } from 'prop-types';
// import Table from "@mui/material/Table";
// import TableBody from "@mui/material/TableBody";
// import TableCell from "@mui/material/TableCell";
// import TableContainer from "@mui/material/TableContainer";
// import TableHead from "@mui/material/TableHead";
// import TableRow from "@mui/material/TableRow";
// import Paper from "@mui/material/Paper";
import { Box } from '@mui/material';
import { Typography } from '@mui/material';
import RecipeStep from './RecipeStep';
import RecipeTimeline from '../recipeComponents/RecipeTimeline';
import Grid from '@mui/material/Unstable_Grid2';
import moment from 'moment';
export default function RecipeProcedure(props) {
  const { steps } = props.procedure;
  
  return (
    <Box>
      <Grid container spacing={1}>
        <Grid xs={10}>
          <Typography variant="h6">{props.procedure.name}</Typography>
          <Typography variant="body1">{props.procedure.description}</Typography>
          <React.Fragment>
            {steps.map((step) => (
              <Box key={step.id} sx={{ mt: "5px" }}>
                <RecipeStep step={step} />
                {/* <Divider /> */}
              </Box>
            ))}
          </React.Fragment>
        </Grid>
        <Grid xs={2} >
          <RecipeTimeline
            items={generateItems(steps)}
          />
        </Grid>
      </Grid>
    </Box>
  );
}

function generateItems(steps) {
  var d = new moment("2014-01-01 10:11:55");
  d = d.add(10, "seconds");
  let items = [];
  steps.forEach(step => {
    items.push({
      val: d.add( step.duration_in_seconds, "seconds").format("HH:mm"),
      main: false,
      connector: true,
    });    
  });
  return items;
}

RecipeProcedure.propTypes = {
    procedure: PropTypes.object.isRequired,
};
