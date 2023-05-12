import React from "react";
import PropTypes from "prop-types";
import { useCallback } from "react";
import { Controller, useFormContext } from "react-hook-form";
import TextField from "@mui/material/TextField";
import Stack from "@mui/material/Stack";
import IngredientsTable from "./Ingredients/IngredientsTable";
import get from "lodash/get";

function NewProcedure({ procedureId }) {
  const { formState, control, watch } = useFormContext();
  const baseName = `procedures.p${procedureId}`;


  watch(`${baseName}.name`);

  const renderTextField = useCallback(
    (name, label, rules, helperText, multiline = false, rows = 1, maxWidth = "250px") => (
      <Controller
        key={name}
        name={`${baseName}.${name}`}
        control={control}
        defaultValue=""
        rules={rules}
        render={({ field }) => (
          <TextField
            {...field}
            color="info"
            label={label}
            multiline={multiline}
            rows={rows}
            helperText={get(formState.errors, `${baseName}.${name}`) && helperText}
            sx={{
              mb: 2,
              maxWidth: { maxWidth },
            }}
          />
        )}
      />
    ),
    [baseName, control, formState]
  );

  return (
    <Stack sx={{ justifyContent: "center" }}>
      {renderTextField(
        "name",
        "Name",
        { required: true, maxLength: 30 },
        "Please enter a name for your recipe (max 50 characters)"
      )}
      {renderTextField(
        "description",
        "Description",
        { required: true, maxLength: 200 },
        "Please enter a description for your recipe (max 200 characters)",
        true,
        4,
        "500px"
      )}
      <IngredientsTable />
    </Stack>
  );
}

NewProcedure.propTypes = {
  procedureId: PropTypes.number.isRequired,
};

export default React.memo(NewProcedure);
