import { TextField, TableCell } from '@mui/material';
import PropTypes from 'prop-types';

const IngredientCell = ({ value, index, editIndex, handleEdit }) => {
    return (
        <TableCell>
            {editIndex === index ? (
                <TextField
                    value={value}
                    onChange={(event) => handleEdit(index, event.target.value)}
                />
            ) : (
                    value
            )}
        </TableCell>
    );
};

export default IngredientCell;

IngredientCell.propTypes = {
    value: PropTypes.any.isRequired,
    index: PropTypes.number.isRequired,
    editIndex: PropTypes.number.isRequired,
    handleEdit: PropTypes.func.isRequired,
};
