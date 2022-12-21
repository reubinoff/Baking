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

export default function RecipeStep(props) {
  return (
    <Box>
      <Typography variant="subtitle1">{props.step.name}</Typography>
      <Typography variant="body1">{props.step.description}</Typography>
    </Box>
  );
}

RecipeStep.propTypes = {
  step: PropTypes.object.isRequired,
};
