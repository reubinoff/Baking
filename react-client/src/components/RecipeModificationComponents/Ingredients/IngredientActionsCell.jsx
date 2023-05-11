import { TableCell, IconButton } from '@mui/material';
import { Edit, Save, Delete } from '@mui/icons-material';
import { ButtonGroup } from '@mui/material';
import PropTypes from 'prop-types';

function IngredientActionsCell({ index, editIndex, handleEditClick, handleDelete, handleSaveClick }) {
    return (
        <TableCell align="right">
            <ButtonGroup variant="text" size='small' >
                {editIndex === index ? (
                    <IconButton onClick={() => handleSaveClick(index)}>
                        <Save />
                    </IconButton>
                ) : (
                    <IconButton onClick={() => handleEditClick(index)}>
                        <Edit />
                    </IconButton>
                )}
                <IconButton style={{'display': editIndex !== index ? 'none' : ''}}
                     onClick={() => handleDelete(index)}>
                    <Delete />
                </IconButton>
            </ButtonGroup>
        </TableCell>
    );
}

export default IngredientActionsCell;

IngredientActionsCell.propTypes = {
    index: PropTypes.number.isRequired,
    editIndex: PropTypes.number.isRequired,
    handleEditClick: PropTypes.func.isRequired,
    handleDelete: PropTypes.func.isRequired,
    handleSaveClick: PropTypes.func.isRequired,
};
