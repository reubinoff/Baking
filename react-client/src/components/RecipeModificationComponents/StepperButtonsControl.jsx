
import { PropTypes } from "prop-types";
import { Button } from "@mui/material";
import Box from "@mui/material/Box";



export default function StepperButtonsControl(props) {
  const {
    activeStep,
    handleNext,
    handleBack,
    isLastStep,
    disabled,
    errors } = props;
  return (
    (
      <Box sx={{ mb: 2 }}>
        <div>

          <Button

            disabled={Object.keys(errors).length !== 0}
            onClick={handleBack}
            sx={{ mt: 1, mr: 1, display: activeStep === 0 ? "none" : "inline-flex" }}
          >
            Back
          </Button>
          <Button
            variant="contained"
            onClick={handleNext}
            sx={{ mt: 1, mr: 1 }}
            type={isLastStep ? "submit" : "button"}
            disabled={Object.keys(errors).length !== 0 || disabled}
          >
            {isLastStep ? "Submit" : "Next"}
          </Button>
        </div>
      </Box>
    )
  );
}

StepperButtonsControl.propTypes = {
  activeStep: PropTypes.number.isRequired,
  handleNext: PropTypes.func.isRequired,
  handleBack: PropTypes.func.isRequired,
  isLastStep: PropTypes.bool,
  disabled: PropTypes.bool.isRequired,
  errors: PropTypes.object
};
StepperButtonsControl.defaultProps = {
  isLastStep: false,
  errors: {}
};
