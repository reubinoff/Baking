import { useState } from "react";
import {
  Stepper,
  Step,
  StepLabel,
  TextField,
  StepContent,
} from "@mui/material";
import { useForm } from "react-hook-form";
import StepperButtonsControl from "./StepperButtonsControl";
import NewRecipeBasicInfo from "./NewRecipeBasicInfo";


const NewRecipeMain = () => {
  const [activeStep, setActiveStep] = useState(0);

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const onSubmit = (data) => {
    console.log(data);
  };

  const steps = [
    {
      label: "Basic info",
      content: <NewRecipeBasicInfo register={register} errors={errors} />,
    },
    {
      label: "Step 2",
      content: (
        <TextField
          {...register("tetete", { required: true, maxLength: 5 })}
          id="tetete"
          label="tetete"
        />
      ),
    },
  ];

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <Stepper activeStep={activeStep} orientation="vertical">
        {steps.map(({ label, content }) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
            <StepContent>
              {content}
              <StepperButtonsControl
                activeStep={activeStep}
                handleNext={handleNext}
                handleBack={handleBack}
                isLastStep={activeStep === steps.length-1}
                errors={errors}
              />
            </StepContent>
          </Step>
        ))}
      </Stepper>
    </form>
  );
};

export default NewRecipeMain;
