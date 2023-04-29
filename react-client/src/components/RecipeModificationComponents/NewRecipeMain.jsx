import { useState, useCallback , useEffect} from "react";
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
import NewProcedure from "./NewProcedure";

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

  
  const GenerateProcedure = (
    (procedureName) => {
      return {
        label: procedureName,
        content: (
          <div>
          <NewProcedure

            register={methods.register}
            errors={methods.formState.errors}
          />
          <Button onClick={AddStep}>Add Step</Button>
        </div>
        ),
      };
    }
  );
    const AddStep = () => {
      const procedureName = `Procedure ${steps.length}`;
      setSteps((prevSteps) => [
        ...prevSteps,
        GenerateProcedure(procedureName),
      ]);
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
    GenerateProcedure("Procedure 1"),
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
