import { PropTypes } from "prop-types";

import { Box, Divider } from "@mui/material";
import { Paper } from "@mui/material";
import Typography from "@mui/material/Typography";
import RecipeIngridients from "./RecipeIngridients";
import RecipeProcedure from "./RecipeProcedure";
import moment from "moment";
import ImageList from "@mui/material/ImageList";
import ImageListItem from "@mui/material/ImageListItem";
export default function RecipeView(props) {
  const { recipe } = props;
  var d = new moment();
  const procedures = recipe.procedures.sort((a, b) => {
    return a.order - b.order;
  });
  return (
    <Box>
      <Typography variant="h4">{recipe.name}</Typography>
      <Typography variant="body1">{recipe.description}</Typography>

      <Paper>
        <Typography variant="h5" sx={{ ml: "5px" }}>
          Ingredients
          <RecipeIngridients
            ingredients={recipe.ingredients}
            currentHyration={recipe.hydration}
            reqTotalLoafWeight={props.reqTotalLoafWeight}
            reqHyration={props.reqHyration}
            reqTotalLoafCount={props.reqTotalLoafCount}
          />
        </Typography>
      </Paper>
      <Box sx={{ mt: 5 }}>
        <Typography variant="h5" sx={{ ml: "5px" }}>
          Procedures
          {procedures.map((procedure, idx) => {
            if (idx > 0) {
              d = d.add(procedures[idx - 1].duration_in_seconds, "seconds");
            }
            return (
              <Box key={procedure.name} sx={{ mt: "20px" }}>
                <RecipeProcedure procedure={procedure} startTimestamp={d} />
                <Divider />
              </Box>
            );
          })}
        </Typography>
      </Box>
      <ImageList
        gap={12}
        sx={{
          mb: 8,
          gridTemplateColumns:
            "repeat(auto-fill, minmax(150px, 1fr))!important",
        }}
        rowHeight={164}
      >
        <ImageListItem key={recipe.name} sx={{ height: "100% !important" }}>
          <img
            src={`${recipe.cdn_url}?w=164&h=164&fit=crop&auto=format`}
            srcSet={`${recipe.cdn_url}?w=164&h=164&fit=crop&auto=format&dpr=2 2x`}
            alt={recipe.name}
            loading="lazy"
          />
        </ImageListItem>
      </ImageList>
    </Box>
  );
}

RecipeView.propTypes = {
  recipe: PropTypes.object.isRequired,
  reqHyration: PropTypes.number.isRequired, // undefined for same as recipe
  reqTotalLoafWeight: PropTypes.number.isRequired, // undefined for same as recipe
  reqTotalLoafCount: PropTypes.number.isRequired, // undefined for same as recipe
};
