import { Link, useLocation } from "react-router-dom";
import _ from "lodash";

import Table from "@mui/material/Table";
import TableBody from "@mui/material/TableBody";
import TableCell from "@mui/material/TableCell";
import TableContainer from "@mui/material/TableContainer";
import TableHead from "@mui/material/TableHead";
import TableRow from "@mui/material/TableRow";
import Paper from "@mui/material/Paper";


function Recipe() {
const { state } = useLocation();
    if ( _.isUndefined( state?.recipe)) {
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
      </div>
      <p>
        <Link to="/">Go to the home page</Link>
      </p>
    </div>
  );
}

function t(recipe) {
  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="simple table">
        <TableHead>
          <TableRow>
            <TableCell>Name</TableCell>
            <TableCell >Description</TableCell>
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
              <TableCell >{row.description}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
}
export default Recipe;
