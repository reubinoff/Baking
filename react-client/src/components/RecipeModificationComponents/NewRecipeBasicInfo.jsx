import { PropTypes } from "prop-types";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";
import FileUpload from "../recipeComponents/FileUpload";

export default function NewRecipeBasicInfo(props) {
  const { register,errors } = props
  return (
    //Add Centered Container
    <Box sx={{ justifyContent: "center" }}>
      <TextField
        color="info"
        error={
          errors?.Name?.type === "maxLength" ||
          errors?.Name?.type === "required"
        }
        {...register("Name", { required: true, maxLength: 5 })}
        id="Name"
        label="Name"
        helperText={
          errors?.Name?.type === "maxLength" &&
          "Please enter a name for your recipe (max 5 characters)"
        }
        sx={{ mb: 2 }}
      />
      <TextField
        color="info"
        error={
          errors?.Desctiption?.type === "maxLength" ||
          errors?.Desctiption?.type === "required"
        }
        {...register("Desctiption", { required: true, maxLength: 100 })}
        id="Desctiption"
        label="Desctiption"
        multiline
        rows={4}
        helperText= "Please enter a description for your recipe (max 100 characters)"
        sx={{ mb: 2 }}
      />
      <FileUpload limit={3} multiple name="images" />
    </Box>
  );
}

NewRecipeBasicInfo.propTypes = {
  register : PropTypes.func.isRequired,
  errors : PropTypes.object.isRequired
};