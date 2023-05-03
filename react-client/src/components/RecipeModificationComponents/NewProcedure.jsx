
import PropTypes from "prop-types";
import TextField from "@mui/material/TextField";
import Box from "@mui/material/Box";
import IngredientsTable from "./Ingredients/IngredientsTable";



export default function NewProcedure(props) {
  const { register, errors } = props;
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
        helperText="Please enter a description for your recipe (max 100 characters)"
        sx={{ mb: 2 }}
      />
      <IngredientsTable />
    </Box>
  );
}

NewProcedure.propTypes = {
  register: PropTypes.func.isRequired,
  errors: PropTypes.object.isRequired,
};