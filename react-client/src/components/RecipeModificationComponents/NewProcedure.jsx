

export default function NewProcedure(props) {
  const [open, setOpen] = React.useState(false);
  const [data , setData] = React.useState(null);
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm();
  const onSubmit = (data) => {
    console.log(data);
    setData(data);
    setOpen(true);
  };

  return (
    //Add Centered Container
    <Box sx={{ display: "flex", justifyContent: "center" }}>

      <form onSubmit={handleSubmit(onSubmit)}>
        <div>
          <TextField
            color="info"
            error={
              errors?.Name?.type === "maxLength" ||
              errors?.Name?.type === "required"
            }
            {...register("Name", { required: true, maxLength: 5 })}
            id="Name"
            label="Name"
            helperText="Please enter a name for your recipe (max 5 characters)"
          />
        </div>

        <div>
          <TextField
            color="info"
            error={
              errors?.Desctiption?.type === "maxLength" ||
              errors?.Desctiption?.type === "required"
            }
            {...register("Desctiption", { required: true, maxLength: 100 })}
            id="Desctiption"
            label="Desctiption"
            multiline
            rows={4}
            helperText="Please enter a Desctiption for your recipe (max 100 characters)"
          />
        </div>

        <div>
          <TextField
            color="info"
            error={
              errors?.Ingredients?.type === "maxLength" ||
              errors?.Ingredients?.type === "required"
            }
            {...register("Ingredients", { required: true, maxLength: 100 })}
            id="Ingredients"
            label="Ingredients"
            multiline
            rows={4}
            helperText="Please enter a Ingredients for your recipe (max 100 characters)"
          />
        </div>

        <div>
          <TextField
            color="info"
            error={
              errors?.Procedure?.type === "maxLength" ||
              errors?.Procedure?.type === "required"
            }
            {...register("Procedure", { required: true, maxLength: