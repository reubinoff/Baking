import { useState } from "react";
import {
  Stepper,
  Step,
  StepLabel,
  TextField,
  StepContent,
  Button,
} from "@mui/material";
import { useForm, FormProvider } from "react-hook-form";
import StepperButtonsControl from "./StepperButtonsControl";
import NewRecipeBasicInfo from "./NewRecipeBasicInfo";

const NewRecipeMain = () => {
  const [activeStep, setActiveStep] = useState(0);

  const methods = useForm({
    mode: "onChange",
  });

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const onSubmit = (data) => {
    console.log(data);
  };

  const AddStep = () => {
    console.log("AddStep");
    const newStep = {
      label: "Step 3",
      content: (
        <div>
          <TextField
            {...methods.register("tetete", { required: true, maxLength: 5 })}
            id="tetete"
            label="tetete"
          />
        </div>
      ),
    };
    setSteps([...steps, newStep]);
  };
  const [steps, setSteps] = useState([
    {
      label: "Basic info",
      content: (
        <NewRecipeBasicInfo
          register={methods.register}
          errors={methods.formState.errors}
        />
      ),
    },
    {
      label: "Step 2",
      content: (
        <div>
          <TextField
            {...methods.register("tetete", { required: true, maxLength: 5 })}
            id="tetete"
            label="tetete"
          />
          <Button variant="contained" onClick={AddStep}>
            Add
          </Button>
        </div>
      ),
    },
  ]);

  return (
    <FormProvider {...methods}>
      <Stepper activeStep={activeStep} orientation="vertical">
        {steps.map(({ label, content }) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
            <StepContent>
              {content}
              <StepperButtonsControl
                activeStep={activeStep}
                handleNext={activeStep === steps.length - 1 ? methods.handleSubmit(onSubmit) : handleNext}
                handleBack={handleBack}
                isLastStep={activeStep === steps.length - 1}
                errors={methods.formState.errors}
              />
            </StepContent>
          </Step>
        ))}
      </Stepper>
    </FormProvider>
  );
};

export default NewRecipeMain;
