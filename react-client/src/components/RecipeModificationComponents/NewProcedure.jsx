import React from "react";
import PropTypes from "prop-types";
import { useFormContext } from "react-hook-form";
import Stack from "@mui/material/Stack";
import IngredientsTable from "./Ingredients/IngredientsTable";
import BaseFormTextField from "./BaseFormTextField";
import StepsList from "./steps/StepsList";

function NewProcedure({ procedureId }) {
  const { watch } = useFormContext();
  const baseName = `procedures.p${procedureId}`;


  watch(`${baseName}.name`);

  return (
    <Stack sx={{ justifyContent: "center" }}>
      {
        <BaseFormTextField
          baseName={baseName}
          name="name"
          label="Name"
          rules={{ required: true, maxLength: 30 }}
          helperText="Please enter a name for your recipe (max 50 characters)" />
      }
      {
        <BaseFormTextField
          baseName={baseName}
          name="description"
          label="Description"
          rules={{ required: true, maxLength: 200 }}
          helperText="Please enter a description for your recipe (max 200 characters)"
          multiline={true}
          rows={4}
          maxWidth="500px"
        />
      }
      <IngredientsTable />
      <StepsList />
    </Stack>
  );
}

NewProcedure.propTypes = {
  procedureId: PropTypes.number.isRequired,
};

export default React.memo(NewProcedure);
