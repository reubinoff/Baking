import PropTypes from "prop-types";
import React from "react";
import Box from "@mui/material/Box";
import Grid from "@mui/material/Unstable_Grid2"; // Grid version 2

export default function PlaceholderItems(props) {
  const { placeholder, total, ready } = props;

  return (
    <Box sx={{ flexGrow: 1 }}>
      {!ready && (
        <Grid spacing={2}>
          {[...new Array(total).keys()].map((i) => (
            <Grid xs={12} md={3} key={i}>
              {React.createElement(placeholder, { key: i })}
            </Grid>
          ))}
        </Grid>
      )}
    </Box>
  );
}

PlaceholderItems.propTypes = {
  placeholder: PropTypes.func.isRequired,
  total: PropTypes.number.isRequired,
  ready: PropTypes.bool.isRequired,
};

// defulat values
PlaceholderItems.defaultProps = {
  total: 5,
};
