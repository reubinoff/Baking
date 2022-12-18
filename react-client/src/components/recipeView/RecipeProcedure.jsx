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
import Divider from '@mui/material/Divider';

export default function RecipeProcedure(props) {
  return (
    <Box>
      <Typography variant="h6">{props.procedure.name}</Typography>
      <Typography variant="body1">{props.procedure.description}</Typography>
      <Box>
        {props.procedure.steps.map((step) => (
          <Box key={step.id}>
            <RecipeStep step={step} />
            <Divider />
          </Box>
        ))}
      </Box>
    </Box>
  );
}

RecipeProcedure.propTypes = {
    procedure: PropTypes.object.isRequired,
};
