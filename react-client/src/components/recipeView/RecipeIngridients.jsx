import { PropTypes } from 'prop-types';
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import { Box } from '@mui/material';
export default function RecipeIngridients(props) {
  return (
    <Box>
      <TableContainer component={Paper}>
        <Table aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Quantity</TableCell>
              <TableCell>Type</TableCell>
              <TableCell>Precentage</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {props.ingredients.map((row) => (
              <TableRow
                key={row.name}
                sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
              >
                <TableCell component="th" scope="row">
                  {row.name}
                </TableCell>
                <TableCell>{row.quantity}</TableCell>
                <TableCell>{row.type}</TableCell>
                <TableCell>0%</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
}

RecipeIngridients.propTypes = {
  ingredients: PropTypes.array.isRequired,
  total_weight_per_loaf: PropTypes.number, // undefined for same as recipe
};
