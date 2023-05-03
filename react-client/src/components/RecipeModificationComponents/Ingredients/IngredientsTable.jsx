import { Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper } from '@mui/material';
import { Button } from '@mui/material';
import IngredientCell from './IngredientCell';
import IngredientActionsCell from './IngredientActionsCell';
import { useState } from 'react';



const IngredientsTable = () => {
    const [ingredients, setIngredients] = useState([
        { name: 'Flour', quantity: 1, unit: 'cup', type: 'Dry' },
    ]);
    const [editIndex, setEditIndex] = useState(-1);

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
        const newIngredient = { name: '', quantity: '', unit: '', type: '' };
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
                        <TableCell>Name</TableCell>
                        <TableCell>Quantity</TableCell>
                        <TableCell>Unit</TableCell>
                        <TableCell>Type</TableCell>
                        <TableCell></TableCell>
                    </TableRow>
                </TableHead>
                <TableBody>
                    {ingredients.map((ingredient, index) => (
                        <TableRow key={index}>
                            {['name', 'quantity', 'unit', 'type'].map((key) => (
                                <IngredientCell
                                    key={key}
                                    value={ingredient[key]}
                                    index={index}
                                    editIndex={editIndex}
                                    handleEdit={(index, value) => handleEdit(index, key, value)}
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
