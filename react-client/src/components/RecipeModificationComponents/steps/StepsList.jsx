import React, { useState } from "react";
import { Typography, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, TextField, IconButton, Box } from "@mui/material";
import { AddCircleOutlineOutlined } from "@mui/icons-material";

export default function StepsList() {
    const [steps, setSteps] = useState([{ description: "", duration: "" }]);

    const handleAddStep = () => {
        setSteps((prevSteps) => [...prevSteps, { description: "", duration: "" }]);
    };

    const handleStepChange = (index, field, value) => {
        setSteps((prevSteps) => {
            const newSteps = [...prevSteps];
            newSteps[index][field] = value;
            return newSteps;
        });
    };

    return (
        <React.Fragment>
            <Typography variant="h6">Steps</Typography>
            <TableContainer component={Paper}>
                <Table style={{ borderCollapse: "collapse", cellSpacing: 0 }} size="small" >
                    <TableHead>
                        <TableRow>
                            <TableCell width="100%">Description</TableCell>
                            <TableCell>dur <Typography variant="body2" style={{ alignSelf: "flex-end", marginLeft: "4px" }}>
                                (min)
                            </Typography></TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {steps.map((step, index) => (
                            <TableRow key={index}>
                                <TableCell size="small">
                                    <TextField
                                        multiline
                                        value={step.description}
                                        onChange={(e) => handleStepChange(index, "description", e.target.value)}
                                        rows={3}
                                        inputProps={{ style: { fontSize: 14 } }}
                                        variant="standard"
                                        style={{ width: "100%", border: "none" }}
                                    />
                                </TableCell>
                                <TableCell style={{ textAlign: "center" }}>
                                    <React.Fragment >
                                        <TextField
                                            type="number"
                                            value={step.duration}
                                            onChange={(e) => handleStepChange(index, "duration", e.target.value)}
                                            style={{ width: "100%", border: "none" }}
                                            variant="standard"

                                            inputProps={{ style: { fontSize: 14, textAlign: "center" } }}

                                        />

                                    </React.Fragment>
                                </TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
            <Box paddingLeft={"16px"}>
                <IconButton size='small' variant="outlined" onClick={handleAddStep}>
                    <AddCircleOutlineOutlined />
                </IconButton>
            </Box>
        </React.Fragment>
    );
}