import PropTypes from "prop-types";
import { Controller, useFormContext } from "react-hook-form";
import TextField from "@mui/material/TextField";
import get from "lodash/get";

export default function BaseFormTextField({ baseName, name, label, rules, helperText, multiline = false, rows = 1, maxWidth = "250px" }) {
    const { formState, control } = useFormContext();
    return (
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
    );
}

BaseFormTextField.propTypes = {
    baseName: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired,
    rules: PropTypes.object.isRequired,
    helperText: PropTypes.string.isRequired,
    multiline: PropTypes.bool,
    rows: PropTypes.number,
    maxWidth: PropTypes.string,
};
BaseFormTextField.defaultProps = {
    multiline: false,
    rows: 1,
    maxWidth: "250px",
};