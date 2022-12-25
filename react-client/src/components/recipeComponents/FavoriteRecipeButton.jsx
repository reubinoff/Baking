import { useState } from "react";
import IconButton from "@mui/material/IconButton";
import FavoriteIcon from "@mui/icons-material/Favorite";
import FavoriteBorderIcon from "@mui/icons-material/FavoriteBorder";
import { PropTypes } from "prop-types";
import { SnackbarProvider, useSnackbar } from "notistack";


function FavoriteButton(params) {
    const { enqueueSnackbar } = useSnackbar();

   const [favorite, setFavorite] = useState(params.favorite);

     const handleClick = () => {
      const message ="Recipe " + ( !favorite ? "removed from favorites" : "added to favorites");
      enqueueSnackbar(message);
      setFavorite(!favorite);
       
     };
  return (
    <IconButton aria-label="add to favorites" onClick={handleClick}>
      {favorite ? (
        <FavoriteBorderIcon color="error" />
      ) : (
        <FavoriteIcon color="error" />
      )}
    </IconButton>
  );
}

export default function FavoriteRecipeButton(props) {
  return (
    <SnackbarProvider maxSnack={1} autoHideDuration={1000}>
      <FavoriteButton {...props} />
    </SnackbarProvider>
  );
}

FavoriteRecipeButton.propTypes = {
  favoirite: PropTypes.bool.isRequired,
};
