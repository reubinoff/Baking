import { TextField, TableCell } from '@mui/material';
import PropTypes from 'prop-types';
import MenuItem from '@mui/material/MenuItem';

const IngredientCell = ({ value, index, editIndex, handleEdit, type, options }) => {

    const handleInternalEdit = (e) => handleEdit(index, e.target.value);
    const getEditableComponent = () => {
        switch (type) {
            case 'enum':
                return (
                    <TextField
                        select
                        value={value}
                        onChange={handleInternalEdit}
                    >
                        {options.map((option) => (
                            <MenuItem key={option} value={option}>
                                {option}
                            </MenuItem>
                        ))}
                    </TextField>
                );
            case 'number':
                return (
                    <TextField
                        type="number"
                        value={value}
                        onChange={handleInternalEdit}
                    />
                );
            default:
                return <TextField value={value} onChange={handleInternalEdit} />;
        }
    };
    return (
        <TableCell>
            {editIndex === index ? (
                getEditableComponent()
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
    type: PropTypes.string.isRequired,
    options: PropTypes.array,
};
