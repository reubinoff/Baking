import React from "react";
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
  const weight_factor = React.useMemo(() => {
    const w = props.total_weight_per_loaf / (1 + (props.required_hydration/100));
    return w;
  }, [props.total_weight_per_loaf, props.required_hydration]);

  return (
    <Box>
      <TableContainer component={Paper}>
        <Table aria-label="simple table">
          <TableHead>
            <TableRow>
              <TableCell>Name</TableCell>
              <TableCell>Orign Quantity</TableCell>
              <TableCell>Calc Quantity</TableCell>
              <TableCell>Precentage</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {props.ingredients.map((ingredient) => (
              <TableRow
                key={ingredient.name}
                sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
              >
                <TableCell component="th" scope="row">
                  {ingredient.name}
                </TableCell>
                <TableCell>{ingredient.quantity}</TableCell>
                <TableCell>{Math.round(weight_factor * ingredient.precentage)}</TableCell>
                <TableCell>
                  {Math.round(ingredient.precentage * 100)}%
                </TableCell>
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
  total_weight_per_loaf: PropTypes.number.isRequired, // undefined for same as recipe
  required_hydration: PropTypes.number.isRequired, // undefined for same as recipe
};
