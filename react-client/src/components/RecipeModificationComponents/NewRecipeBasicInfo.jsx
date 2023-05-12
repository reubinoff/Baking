import FileUpload from "../recipeComponents/FileUpload";
import BaseFormTextField from "./BaseFormTextField";
import { Stack } from "@mui/material";

export default function NewRecipeBasicInfo() {
  return (
    //Add Centered Container
    <Stack sx={{ justifyContent: "center" }}>
      <BaseFormTextField
        baseName="recipe"
        name="name"
        label="Name"
        rules={{ required: true, maxLength: 5 }}
        helperText="Please enter a name for your recipe (max 30 characters)"
      />
      <BaseFormTextField
        baseName="recipe"
        name="description"
        label="Description"
        rules={{ required: true, maxLength: 400 }}
        helperText="Please enter a description for your recipe (max 400 characters)"
        multiline={true}
        rows={4}
        maxWidth="500px"
      />
      <FileUpload limit={3} multiple name="images" />
    </Stack>
  );
}
