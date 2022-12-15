import { Link, useLocation } from "react-router-dom";
import _ from "lodash";

import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";

function getTotalIngredients(recipe) {
  let ingredients = {};
  recipe.procedures.forEach((procedure) => {
    procedure.ingredients.forEach((ingredient) => {
      if (ingredients[ingredient.name]) {
        ingredients[ingredient.name].quantity += ingredient.quantity;
      } else {
        ingredients[ingredient.name] = ingredient;
      }
    });
  });
  return ingredients;
}
function Recipe() {
  const { state } = useLocation();
  const i = getTotalIngredients(state.recipe);
  if (_.isUndefined(state?.recipe)) {
    return (
      <div>
        <h2>Recipe not found</h2>
        <p>
          <Link to="/">Go to the home page</Link>
        </p>
      </div>
    );
  }
  return (
    <div>
      <h2>{state.recipe.name}</h2>
      <div>
        <p>{state.recipe.description}</p>
        {t(state.recipe)}
        {ingredient(Object.values(i))}
      </div>
      <p>
        <Link to="/">Go to the home page</Link>
      </p>
    </div>
  );
}
function ingredient(ingredients) {
  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell>Quantity</TableCell>
            <TableCell>Type</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {ingredients.map((row) => (
            <TableRow
              key={row.name}
              sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {row.name}
              </TableCell>
              <TableCell>{row.quantity}</TableCell>
              <TableCell>{row.type}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}

function t(recipe) {
  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell>Description</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {recipe.procedures.map((row) => (
            <TableRow
              key={row.name}
              sx={{ "&:last-child td, &:last-child th": { border: 0 } }}
            >
              <TableCell component="th" scope="row">
                {row.name}
              </TableCell>
              <TableCell>{row.description}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
export default Recipe;
