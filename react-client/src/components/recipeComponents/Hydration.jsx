
import Box from "@mui/material/Box";
import Typography from "@mui/material/Typography";
import WaterIcon from "@mui/icons-material/Water";
import { PropTypes } from 'prop-types';

export default function Hydration(props){
    const { hydration } = props;
    return (
      <Box display="flex" alignItems="center" {...props}>
        <WaterIcon color="primary" />
        <Typography variant="body2" color="text.secondary">
          {hydration}%
        </Typography>
      </Box>
    );
}

Hydration.propTypes = {
  hydration: PropTypes.number.isRequired,
};