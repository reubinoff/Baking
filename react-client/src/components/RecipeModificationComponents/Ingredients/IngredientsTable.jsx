import { Table, TableBody, TableCell, TableContainer, TableRow, Paper, Typography } from '@mui/material';
import IngredientActionsCell from './IngredientActionsCell';
import { useState } from 'react';
import { IconButton } from '@mui/material';
import { AddCircleOutlineOutlined } from '@mui/icons-material';
import { useFieldArray, useFormContext } from 'react-hook-form';
import propTypes from 'prop-types';
import BaseFormTextField from '../BaseFormTextField';

class IngredientModel {
    constructor(name, quantity, unit, type) {
        this.name = name;
        this.quantity = quantity;
        this.unit = unit;
        this.type = type;
    }
}

const IngredientsTable = ({ formBaseName }) => {
    const { control } = useFormContext();
    const { fields, append, remove, update } = useFieldArray({
        control: control,
        name: formBaseName,
    });

    const [editIndex, setEditIndex] = useState(-1);

    const cells = {
        name:
        {
            name: 'name',
            label: 'Name',
            type: "text",
        },
        quantity:
        {
            name: 'quantity',
            label: 'Qty',
            type: "number",
        },
        unit:
        {
            label: 'Unit',
            name: 'unit',
            type: "enum",
            options: ['cup', 'tsp', 'tbsp', 'oz', 'lb', 'g', 'kg', 'ml', 'l'],
        },
        type:
        {
            label: 'Type',
            name: 'type',
            type: "enum",
            options: ['Dry', 'Wet', 'Dairy', 'Meat', 'Produce', 'Other'],
        },
    };


    const handleDelete = (index) => {
        setEditIndex(-1);
        remove(index);
    };

    const handleAddIngredient = () => {
        const newIngredient = new IngredientModel('', 0, '', '');
        append(newIngredient);
        setEditIndex(fields.length);
    };

    const handleEditClick = (index) => {
        setEditIndex(index);
    };

    const handleSaveClick = (index) => {
        setEditIndex(-1);
        const newFields = [...fields];
        update(newFields);

    };

    const getIngredientCell = (cell, index, val) => {
        const isEditing = index === editIndex;

        if (isEditing) {
            return (
                <TableCell key={cell.label}>
                    <BaseFormTextField
                        key={cell.label}
                        baseName={`${formBaseName}.${index}`}
                        name={cell.name}
                        label={cell.label}
                        options={cell.options}
                        size='small'
                        fieldType={cell.type}
                        maxWidth='100px'
                        rules={{ required: true, maxLength: 30 }}
                        helperText="Please enter a name for your recipe (max 30 characters)"
                    />
                </TableCell>
            );
        }
        else {
            return (
                <TableCell key={cell.label}
                >{val[cell.name]}</TableCell>
            );
        }
    };

    return (
        <Paper sx={{ width: '100%', overflow: 'hidden' }}>
            <Typography variant="h6">Ingredients</Typography>

            <TableContainer component={Paper}>

                <Table size="small" aria-label="Ingredients table">
                    <caption >
                        <IconButton size='small' variant="outlined" onClick={handleAddIngredient}>
                            <AddCircleOutlineOutlined />
                        </IconButton>
                    </caption>

                    <TableBody sx={{ marginTop: '10px' }}>
                        {fields.map((ingredient, index) => (
                            // getIngredientCell(ingredient, index) 
                            <TableRow key={index}>
                                {
                                    Object.keys(cells).map((key) => {
                                        const cell = cells[key];
                                        return getIngredientCell(cell, index, ingredient);
                                    })
                                }
                                <IngredientActionsCell
                                    index={index}
                                    editIndex={editIndex}
                                    handleEditClick={handleEditClick}
                                    handleDelete={handleDelete}
                                    handleSaveClick={handleSaveClick}
                                />
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Paper>
    );
};

IngredientsTable.propTypes = {
    formBaseName: propTypes.string.isRequired,
};


export default IngredientsTable;
