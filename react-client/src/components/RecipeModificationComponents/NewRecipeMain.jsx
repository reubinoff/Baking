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
    defaultValues: {
      'procedures': {}
    }
  });

  const GetNewCompoentn = useCallback(
    (procedureId) => {
      return {
        content: (
            <NewProcedure
            procedureId={procedureId}
            />
        ),
      };
    },
    []
  );

  const [procedures, setprocedures] = useState([
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
      content: (
        <NewProcedure
          procedureId={procedureId}
        />
      ),
    },
  ]);

  const removeProcedure = () => {
      setProcedureId((prev) => prev - 1);
    setprocedures((prev) => prev.filter((_, index) => index !== activeStep));
  };

  useEffect(() => {
    if (procedureId === procedures.length) {
      setprocedures((prev) => [...prev, GetNewCompoentn(procedureId)]);
    }
  }, [procedureId, GetNewCompoentn, procedures.length]);

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
        {procedures.map(({ label, content }, index) => (
          <Step key={index}>
            <StepLabel>{methods.getValues(`procedures.p${content.props.procedureId}.name`) ? methods.getValues(`procedures.p${content.props.procedureId}.name`) : label}
              <Box
                sx={{ float: 'right', display: (index !== activeStep || index === 0) ? "none" : "inline-flex" }}>
                <ButtonGroup>
                  <IconButton size='small' variant="outlined" onClick={removeProcedure} disabled={procedures.length < 3 ? true : false}>
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
                  index === procedures.length - 1
                    ? methods.handleSubmit(onSubmit)
                    : handleNext
                }
                handleBack={handleBack}
                isLastStep={index === procedures.length - 1}
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
