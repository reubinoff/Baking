import React from "react";
import { PropTypes } from "prop-types";
import { useForm } from "react-hook-form";
import TextField from "@mui/material/TextField";
import { Button } from "@mui/material";
import Box from "@mui/material/Box";
import Dialog from "@mui/material/Dialog";
import FileUpload from "../recipeComponents/FileUpload";

export default function NewRecipeMain(props) {
    const [open, setOpen] = React.useState(false);
    const [data , setData] = React.useState(null);
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();
  const onSubmit = (data) => {
    console.log(data);
    setData(data);
    setOpen(true);
  };

  return (
    //Add Centered Container
    <Box sx={{ display: "flex", justifyContent: "center" }}>
      <Dialog
        open={open}
        // onClose={() => setOpen(false)}
      >
        {JSON.stringify(data)}
        <Button onClick={() => setOpen(false)}>Close</Button>
      </Dialog>

      <form onSubmit={handleSubmit(onSubmit)}>
        <div>
          <TextField
            color="info"
            error={
              errors?.Name?.type === "maxLength" ||
              errors?.Name?.type === "required"
            }
            {...register("Name", { required: true, maxLength: 5 })}
            id="Name"
            label="Name"
            helperText="Please enter a name for your recipe (max 5 characters)"
          />
        </div>

        <div>
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
            helperText="Please enter a Desctiption for your recipe (max 100 characters)"
          />
        </div>
        <FileUpload limit={3} multiple name="images" />
        <Button type="submit" variant="contained">
          Submit
        </Button>
      </form>
    </Box>
  );
}

NewRecipeMain.propTypes = {
  name: PropTypes.string,
};
