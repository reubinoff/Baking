import PropTypes from "prop-types";
import { Controller, useFormContext } from "react-hook-form";
import TextField from "@mui/material/TextField";
import get from "lodash/get";
import { MenuItem } from "@mui/material";

export default function BaseFormTextField({
    baseName,
    name,
    label,
    rules,
    helperText,
    size = "medium",
    fieldType = "text",
    options = [],
    multiline = false,
    rows = 1,
    maxWidth = "250px"
}) {
    const { formState, control } = useFormContext();

    const absuluteName = !baseName ? `${name}` : `${baseName}.${name}`;

    const getControllerField = (field) => {
        if (fieldType === "text" || fieldType === "number") {
            return (
                <TextField
                    {...field}
                    size={size}
                    color="info"
                    type={fieldType}
                    label={label}
                    multiline={multiline}
                    rows={rows}
                    error={get(formState.errors, absuluteName) ? true : false}
                    helperText={get(formState.errors, absuluteName) && helperText}
                    sx={{
                        mb: 2,
                        maxWidth: { maxWidth },
                    }}
                />
            );
        }
        if (fieldType === "enum") {
            return (
                <TextField
                    {...field}
                    size={size}
                    label={label}
                    select
                    variant="outlined"
                    fullWidth
                    sx={{
                        mb: 2,
                        maxWidth: { maxWidth },
                    }}
                >
                    {options.map((option) => (
                        <MenuItem key={option} value={option}>
                            {option}
                        </MenuItem>
                    ))}
                
                </TextField>
            );
        }
    }
    return (
        <Controller
            key={name}
            name={absuluteName}
            control={control}
            defaultValue=""
            rules={rules}
            render={({ field }) => getControllerField(field)}
        />
    );
}

BaseFormTextField.propTypes = {
    baseName: PropTypes.string.isRequired,
    name: PropTypes.string.isRequired,
    label: PropTypes.string.isRequired,
    rules: PropTypes.object.isRequired,
    helperText: PropTypes.string.isRequired,
    size: PropTypes.string,
    fieldType: PropTypes.string,
    options: PropTypes.array,
    multiline: PropTypes.bool,
    rows: PropTypes.number,
    maxWidth: PropTypes.string,
};
BaseFormTextField.defaultProps = {
    multiline: false,
    rows: 1,
    maxWidth: "250px",
    size: "medium",
    fieldType: "text",
    options: [],
};