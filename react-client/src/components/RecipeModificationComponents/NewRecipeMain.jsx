import { useState, useCallback, useEffect } from "react";
import {
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Button,
} from "@mui/material";
import { useForm, FormProvider } from "react-hook-form";
import StepperButtonsControl from "./StepperButtonsControl";
import NewRecipeBasicInfo from "./NewRecipeBasicInfo";
import NewProcedure from "./NewProcedure";

const NewRecipeMain = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [procedureId, setProcedureId] = useState(1);
  const methods = useForm({
    mode: "onChange",
  });

  const GetLastProcedureID = useCallback(() => {
    return procedureId;
  }, [procedureId]);

  useEffect(() => {
    if (GetLastProcedureID() > 1) {
      setSteps((prev) => [
        ...prev,
        {
          label: "Procedure" + GetLastProcedureID(),
          content: (
            <div>
              <NewProcedure
                register={methods.register}
                errors={methods.formState.errors}
              />
              <Button onClick={() => setProcedureId((prev) => prev + 1)}>
                Add Step
              </Button>
            </div>
          ),
        },
      ]);
    }
  }, [GetLastProcedureID, methods.register, methods.formState.errors]);


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
      label: "Procedure 1",
      content: (
        <div>
          <NewProcedure
            register={methods.register}
            errors={methods.formState.errors}
          />
          <Button onClick={() => setProcedureId((prev) => prev + 1)}>
            Add Step
          </Button>
        </div>
      ),
    },
  ]);

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const onSubmit = (data) => {
    console.log(data);
  };

  return (
    <FormProvider {...methods}>
      <Stepper activeStep={activeStep} orientation="vertical">
        {steps.map(({ label, content }, index) => (
          <Step key={label}>
            <StepLabel>{label}</StepLabel>
            <StepContent>
              {content}
              <StepperButtonsControl
                activeStep={activeStep}
                handleNext={
                  index === steps.length - 1
                    ? methods.handleSubmit(onSubmit)
                    : handleNext
                }
                handleBack={handleBack}
                isLastStep={index === steps.length - 1}
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
