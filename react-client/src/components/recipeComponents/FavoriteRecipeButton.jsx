import { useState } from "react";
import IconButton from "@mui/material/IconButton";
import FavoriteIcon from "@mui/icons-material/Favorite";
import FavoriteBorderIcon from "@mui/icons-material/FavoriteBorder";
import { PropTypes } from "prop-types";


export default function FavoriteRecipeButton(params) {
   const [favorite, setFavorite] = useState(params.favorite);

  return (
    <IconButton
      aria-label="add to favorites"
      onClick={() => setFavorite(!favorite)}
    >
      {favorite ? (
        <FavoriteBorderIcon color="error" />
      ) : (
        <FavoriteIcon color="error" />
      )}
    </IconButton>
  );
}

FavoriteRecipeButton.propTypes = {
  favoirite: PropTypes.bool.isRequired,
};
