import React from "react";
import { Box } from "@mui/material";
import PropTypes from "prop-types";

import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import FormControl from "@mui/material/FormControl";
import Select from "@mui/material/Select";
import _ from "lodash";

export default function RecipeQuantitySelector(props) {
  const [defaultValues, setDefaultValues] = React.useState({
    reqHyration: props.requiredValues.reqHyration,
    reqTotalLoafWeight: props.requiredValues.reqTotalLoafWeight,
    reqTotalLoafCount: props.requiredValues.reqTotalLoafCount,
  });

  React.useEffect(() => {
    setDefaultValues({
      ...props.requiredValues,
    });
  }, [props, setDefaultValues]);

  const hydrationOptions = React.useMemo(() => {
    const offset = 15;
    const min =
      defaultValues.reqHyration > offset
        ? defaultValues.reqHyration - offset
        : 0;
    const max = defaultValues.reqHyration + offset;
    const step = 1;
    const l = _.range(min, max, step);
    // sort the array
    return l.sort((a, b) => a - b);
  }, [defaultValues]);

  const weightOptions = React.useMemo(() => {
    const min = 100;
    const max = 1000;
    const step = 50;
    const l = _.range(min, max, step);
    if (l.includes(defaultValues.reqTotalLoafWeight) === false) {
      l.push(defaultValues.reqTotalLoafWeight);
    }
    // sort the array
    return l.sort((a, b) => a - b);
  }, [defaultValues]);

  const countOptions = React.useMemo(() => {
    const min = 1;
    const max = 20;
    const step = 1;
    const l = _.range(min, max, step);
    if (l.includes(defaultValues.reqTotalLoafCount) === false) {
      l.push(defaultValues.reqTotalLoafCount);
    }
    // sort the array
    return l.sort((a, b) => a - b);
  }, [defaultValues]);

  const updateRequiredValues = (name, value) => {
    props.setRequiredValues({
      ...props.requiredValues,
      [name]: value,
    });
  };

  const items = [
    {
      label: "setReqHyration",
      value: props.requiredValues.reqHyration,
      onchange: (event) =>
        updateRequiredValues("reqHyration", event.target.value),
      text: "Hyration",
      options: hydrationOptions,
    },
    {
      label: "setReqTotalLoafWeight",
      value: props.requiredValues.reqTotalLoafWeight,
      onchange: (event) =>
        updateRequiredValues("reqTotalLoafWeight", event.target.value),

      text: "Weight",
      options: weightOptions,
    },
    {
      label: "ReqTotalLoafCount",
      value: props.requiredValues.reqTotalLoafCount,
      onchange: (event) =>
        updateRequiredValues("reqTotalLoafCount", event.target.value),

      text: "Count",
      options: countOptions,
    },
  ];

  const getFormControl = (items) => {
    return (
      <FormControl
        key={items.label}
        variant="standard"
        sx={{ m: 1, minWidth: 80 }}
      >
        <InputLabel id={items.label + "-label"}>{items.text}</InputLabel>
        <Select
          labelId={items.label}
          id={items.label}
          value={items.value}
          onChange={items.onchange}
          label={items.text}
        >
          {items.options.map((option) => (
            <MenuItem key={items.label + option.toString()} value={option}>
              {option}
            </MenuItem>
          ))}
        </Select>
      </FormControl>
    );
  };

  return <Box>{items.map((item) => getFormControl(item))}</Box>;
}

RecipeQuantitySelector.propTypes = {
  requiredValues: PropTypes.object.isRequired,
  setRequiredValues: PropTypes.func.isRequired,
};
