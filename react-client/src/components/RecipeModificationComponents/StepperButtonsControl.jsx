
import { PropTypes } from "prop-types";
import { Button } from "@mui/material";
import Box from "@mui/material/Box";



export default function StepperButtonsControl(props) {
  const { activeStep, handleNext, handleBack, isLastStep, errors } = props;
  return (
    console.log(errors),
    <Box sx={{ mb: 2 }}>
      <div>
        <Button
          variant="contained"
          onClick={handleNext}
          sx={{ mt: 1, mr: 1 }}
          type={isLastStep ? "submit" : "button"}
          disabled={Object.keys(errors).length !== 0}
        >
          {isLastStep ? "Submit" : "Next"}
        </Button>
        <Button
          disabled={activeStep === 0}
          onClick={handleBack}
          sx={{ mt: 1, mr: 1 }}
        >
          Back
        </Button>
      </div>
    </Box>
  );
}

StepperButtonsControl.propTypes = {
    activeStep: PropTypes.number.isRequired,
    handleNext: PropTypes.func.isRequired,
    handleBack: PropTypes.func.isRequired,
    isLastStep: PropTypes.bool,
    errors : PropTypes.object
};
StepperButtonsControl.defaultProps = {
  isLastStep: false,
  errors : {}
};
