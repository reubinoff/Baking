import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import IngredientCell, { IngredientTypeEnum } from './IngredientCell';
import IngredientActionsCell from './IngredientActionsCell';
import React, { useState } from 'react';
import { IconButton } from '@mui/material';
import { AddCircleOutlineOutlined } from '@mui/icons-material';

class IngredientModel {
    constructor(name, quantity, unit, type) {
        this.name = name;
        this.quantity = quantity;
        this.unit = unit;
        this.type = type;
    }
}

const IngredientsTable = () => {
    const [ingredients, setIngredients] = useState([
        new IngredientModel('Flour', 12, 'cup', 'Dry'),
    ]);
    const [editIndex, setEditIndex] = useState(-1);

    const cells = [
        {
            label: 'Qty',
            type: IngredientTypeEnum.NUMBER,
        },
        {
            label: 'Unit',
            type: IngredientTypeEnum.ENUM,
            options: ['cup', 'tsp', 'tbsp', 'oz', 'lb', 'g', 'kg', 'ml', 'l'],
        },
        {
            label: 'Type',
            type: IngredientTypeEnum.ENUM,
            options: ['Dry', 'Wet', 'Dairy', 'Meat', 'Produce', 'Other'],
        },
    ];



    const handleDelete = (index) => {
        setEditIndex(-1);
        const newIngredients = [...ingredients];
        newIngredients.splice(index, 1);
        setIngredients(newIngredients);
    };

    const handleEdit = (index, key, value) => {
        const newIngredients = [...ingredients];
        newIngredients[index][key] = value;
        setIngredients(newIngredients);
    };

    const handleAddIngredient = () => {
        const newIngredient = new IngredientModel('', 0, '', '');
        setIngredients([...ingredients, newIngredient]);
        const indexOfNewIngredient = ingredients.length;
        setEditIndex(indexOfNewIngredient);
    };

    const handleEditClick = (index) => {
        setEditIndex(index);
    };

    const handleSaveClick = (index) => {
        setEditIndex(-1);
    };


    return (
        <Paper sx={{ width: '100%', overflow: 'hidden' }}>
            <TableContainer component={Paper}>

                <Table size="small" aria-label="Ingredients table">
                    <caption >
                        <IconButton size='small' variant="outlined" onClick={handleAddIngredient}>
                            <AddCircleOutlineOutlined />
                        </IconButton>
                    </caption>

                    <TableHead>
                        <TableRow>
                            {cells.map((cell) => (
                                <TableCell key={cell.label}>{cell.label}</TableCell>
                            ))}
                            <TableCell></TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>

                        {ingredients.map((ingredient, index) => (
                            <React.Fragment key={index}>
                                <TableRow key={'name' + index}  >
                                    <IngredientCell
                                        key={'name'}
                                        value={ingredient.name}
                                        type={IngredientTypeEnum.STRING}
                                        index={index}
                                        editIndex={editIndex}
                                        handleEdit={(index, value) => handleEdit(index,'name', value)}
                                        span={3}
                                    />
                                </TableRow>
                                <TableRow key={index} >
                                    {cells.map((cell) => (
                                        <IngredientCell
                                            key={cell.label}
                                            value={ingredient[cell.label.toLowerCase()]}
                                            type={cell.type}
                                            index={index}
                                            editIndex={editIndex}
                                            handleEdit={(index, value) => handleEdit(index, cell.label.toLowerCase(), value)}
                                            options={cell.options}
                                        />
                                    ))}
                                    <IngredientActionsCell
                                        index={index}
                                        editIndex={editIndex}
                                        handleEditClick={handleEditClick}
                                        handleDelete={handleDelete}
                                        handleSaveClick={handleSaveClick}
                                    />
                                </TableRow>
                            </React.Fragment>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
        </Paper>
    );
};



export default IngredientsTable;
