import { useState, useCallback, useEffect } from "react";
import { Stepper, Step, StepLabel, StepContent, IconButton, Box, ButtonGroup } from "@mui/material";
import { useForm, FormProvider } from "react-hook-form";
import StepperButtonsControl from "./StepperButtonsControl";
import NewRecipeBasicInfo from "./NewRecipeBasicInfo";
import NewProcedure from "./NewProcedure";
import { AddCircleOutlineOutlined, RemoveCircleOutlineOutlined } from "@mui/icons-material";

const NewRecipeMain = () => {
  const [activeStep, setActiveStep] = useState(0);
  const [procedureId, setProcedureId] = useState(1);
  const methods = useForm({
    mode: "onChange",
  });

  const GetNewCompoentn = useCallback(
    (procedureId) => {
      return {
        label: "Procedure" + procedureId,
        content: (
          <div>
            <NewProcedure
              register={methods.register}
              errors={methods.formState.errors}
            />
          </div>
        ),
      };
    },
    [methods.register, methods.formState.errors]
  );

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
        <NewProcedure
          register={methods.register}
          errors={methods.formState.errors}
        />
      ),
    },
  ]);

  const removeProcedure = () => {
      setProcedureId((prev) => prev - 1);
    setSteps((prev) => prev.filter((_, index) => index !== activeStep));
  };

  useEffect(() => {
    if (procedureId === steps.length) {
      setSteps((prev) => [...prev, GetNewCompoentn(procedureId)]);
    }
  }, [procedureId, GetNewCompoentn, steps.length]);

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
            <StepLabel>{label}
              <Box
                sx={{ float: 'right', display: (index !== activeStep || index === 0) ? "none" : "inline-flex" }}>
                <ButtonGroup>
                  <IconButton size='small' variant="outlined" onClick={removeProcedure} disabled={steps.length < 3 ? true : false}>
                    <RemoveCircleOutlineOutlined />
                  </IconButton>
                  <IconButton size='small' variant="outlined" onClick={() => setProcedureId((prev) => prev + 1)} >
                    <AddCircleOutlineOutlined />
                  </IconButton>
                </ButtonGroup>
              </Box>
            </StepLabel>
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
