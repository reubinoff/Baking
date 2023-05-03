import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import { Button } from '@mui/material';
import IngredientCell from './IngredientCell';
import IngredientActionsCell from './IngredientActionsCell';
import { useState } from 'react';

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
        new IngredientModel('Flour', 1, 'cup', 'Dry'),
    ]);
    const [editIndex, setEditIndex] = useState(-1);

    const cells = [
         {
            label: 'Name',
            type: 'text',
        },
        {
            label: 'Quantity',
            type: 'number',
        },
       {
            label: 'Unit',
            type: 'enum',
            options: ['cup', 'tsp', 'tbsp', 'oz', 'lb', 'g', 'kg', 'ml', 'l'],
        },
         {
            label: 'Type',
            type: 'enum',
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
        <TableContainer component={Paper}>
            <Button variant="contained" color="primary" onClick={handleAddIngredient}>
                Add Ingredient
            </Button>
            <Table aria-label="Ingredients table">
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
                        <TableRow key={index}>
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
                    ))}
                </TableBody>
            </Table>
        </TableContainer>
    );
};

export default IngredientsTable;
