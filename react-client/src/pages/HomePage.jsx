
import  RecipeGrid from "../components/RecipeGrid";
import Page from "./Page";
function HomePage() {
  return <Page title="Baking" content={<RecipeGrid query={""} />} />;
}

export default HomePage;
