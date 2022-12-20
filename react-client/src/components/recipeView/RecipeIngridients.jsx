import React from "react";
import { PropTypes } from "prop-types";
import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";
import { Box } from "@mui/material";

export default function RecipeIngridients(props) {
  const hydrationFactor = React.useMemo(() => {
    if (props.currentHyration === 0) {
      return 0;
    }
    return props.reqHyration / props.currentHyration;
  }, [props.reqHyration, props.currentHyration]);

  const weight_factor = React.useMemo(() => {
    const calculatedHydration = (props.currentHyration / 100) * hydrationFactor;
    const w = props.reqTotalLoafWeight / (1 + calculatedHydration);
    return w * props.reqTotalLoafCount;
  }, [
    props.reqTotalLoafWeight,
    props.reqTotalLoafCount,
    props.currentHyration,
    hydrationFactor,
  ]);

  const calculated_quntity = (ingredient) => {
    if (ingredient?.is_liquid) {
      return Math.round(
        weight_factor * ingredient.precentage * hydrationFactor
      );
    }
    return Math.round(weight_factor * ingredient.precentage);
  };

  return (
    <Box>
      <TableContainer component={Paper}>
        <Table aria-label="ingredients table">
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
                  {ingredient.name} {ingredient.is_liquid.toString()}
                </TableCell>
                <TableCell>{ingredient.quantity}</TableCell>
                <TableCell>{calculated_quntity(ingredient)}</TableCell>
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
  currentHyration: PropTypes.number.isRequired,
  reqTotalLoafWeight: PropTypes.number.isRequired, // undefined for same as recipe
  reqHyration: PropTypes.number.isRequired, // undefined for same as recipe
  reqTotalLoafCount: PropTypes.number.isRequired, // undefined for same as recipe
};
