import { useState } from "react";
import Card from "@mui/material/Card";
import CardHeader from "@mui/material/CardHeader";
import CardMedia from "@mui/material/CardMedia";
import CardContent from "@mui/material/CardContent";
import CardActions from "@mui/material/CardActions";
import Typography from "@mui/material/Typography";
import PropTypes from "prop-types";
import Skeleton from "@mui/material/Skeleton";
import { useNavigate } from "react-router-dom";
import Hydration from "./recipeComponents/Hydration";
import ShareButton from "./recipeComponents/ShareButton";
import FavoriteRecipeButton from "./recipeComponents/FavoriteRecipeButton";
export default function RecipeCard(props) {
  const { recipe } = props;
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  const navigateToRecipe = () => {
    navigate(`/recipe/${recipe.id}`, { state: { recipe: recipe } });
  };

  return (
    <Card>
      <CardHeader
        title={recipe.name}
        action={<Hydration hydration={recipe.hydration} />}
      ></CardHeader>
      <CardMedia
        component="img"
        alt={recipe.name}
        image={recipe.cdn_url}
        onLoad={() => setLoading(false)}
        onClick={navigateToRecipe}
      />
      {loading && <CardMedia variant="top" src="images/placeholder.png" />}
      <Skeleton
        sx={{ height: 190, width: "90%", display: loading ? "block" : "none" }}
        animation="wave"
        variant="rectangular"
      />

      <CardContent onClick={navigateToRecipe}>
        <Typography variant="body2" color="text.secondary">
          {recipe.description}
        </Typography>
      </CardContent>
      <CardActions>
        <FavoriteRecipeButton favoirite={false} />
        <ShareButton recipe_id={recipe.id} recipe_name={recipe.name} />
      </CardActions>
    </Card>
  );
}

RecipeCard.propTypes = {
  recipe: PropTypes.object.isRequired,
};
