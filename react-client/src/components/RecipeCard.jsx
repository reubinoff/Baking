import { useCallback, useState } from "react";
import Card from "@mui/material/Card";
import CardHeader from "@mui/material/CardHeader";
import CardMedia from "@mui/material/CardMedia";
import CardContent from "@mui/material/CardContent";
import CardActions from "@mui/material/CardActions";
import Typography from "@mui/material/Typography";
import PropTypes from "prop-types";
import IconButton from "@mui/material/IconButton";
import FavoriteIcon from "@mui/icons-material/Favorite";
import FavoriteBorderIcon from "@mui/icons-material/FavoriteBorder";
import Skeleton from "@mui/material/Skeleton";
import { useNavigate } from "react-router-dom";
import Hydration from "./recipeComponents/Hydration";
import ShareButton from "./recipeComponents/ShareButton";

export default function RecipeCard(props) {
  const [recipe] = useState(props.recipe);
  const [loading, setLoading] = useState(true);
  const [favorite, setFavorite] = useState(false);
  const navigate = useNavigate();

  const changeFavorite = useCallback((event) => {
    event.stopPropagation();
    setFavorite(!favorite);
  }, [favorite]);

  const handleImageLoaded = useCallback(() => {
    setLoading(false);
  }, []);

  const navigateToRecipe = () => {
    // console.log("navigate to recipe");
    navigate(`/recipe/${recipe.id}`, { state: { recipe: recipe } });
  };

  return (
    <Card >
      <CardHeader
        title={recipe.name}
        action={<Hydration hydration={recipe.hydration} />}
      ></CardHeader>
      <CardMedia
        component="img"
        alt={recipe.name}
        image={recipe.cdn_url}
        onLoad={handleImageLoaded}
        onClick={navigateToRecipe}
      />
      {loading && <CardMedia variant="top" src="images/placeholder.png" />}
      {loading && <Skeleton animation="wave" variant="rectangular" />}

      <CardContent onClick={navigateToRecipe}>
        <Typography variant="body2" color="text.secondary">
          {recipe.description}
        </Typography>
      </CardContent>
      <CardActions>
        <IconButton aria-label="add to favorites" onClick={changeFavorite}>
          {favorite ? (
            <FavoriteBorderIcon color="error" />
          ) : (
            <FavoriteIcon color="error" />
          )}
        </IconButton>
        <ShareButton />
        {/* <IconButton aria-label="share">
          <ShareIcon />
        </IconButton> */}
      </CardActions>
    </Card>
  );
}

RecipeCard.propTypes = {
  recipe: PropTypes.object.isRequired,
};
