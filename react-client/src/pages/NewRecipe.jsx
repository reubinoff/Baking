import Page from "./Page";
import NewRecipeMain from "../components/RecipeModificationComponents/NewRecipeMain";

function NewRecipe() {
  return <Page title="Baking" content={<NewRecipeMain />} />;
}

export default NewRecipe;
