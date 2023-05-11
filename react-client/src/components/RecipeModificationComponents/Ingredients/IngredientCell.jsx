import { TextField, TableCell } from '@mui/material';
import PropTypes from 'prop-types';
import MenuItem from '@mui/material/MenuItem';

export class IngredientTypeEnum {
    static get STRING() {
        return 'string';
    }

    static get NUMBER() {
        return 'number';
    }

    static get ENUM() {
        return 'enum';
    }
}

const IngredientCell = ({ value, index, editIndex, handleEdit, type, options, span }) => {

    const handleInternalEdit = (e) => handleEdit(index, e.target.value);
    const getEditableComponent = () => {
        switch (type) {
            case IngredientTypeEnum.ENUM:
                return (
                    <TextField
                        size='small'
                        select
                        value={value}
                        variant='standard'
                        onChange={handleInternalEdit}
                    >
                        {options.map((option) => (
                            <MenuItem key={option} value={option}>
                                {option}
                            </MenuItem>
                        ))}
                    </TextField>
                );
            case IngredientTypeEnum.NUMBER:
                return (
                    <TextField
                        size='small'
                        variant='standard'
                        type="number"
                        sx={{minWidth: '50px'}}
                        value={value}
                        onChange={handleInternalEdit}
                    />
                );
            default:
                return <TextField variant='standard' size='small' value={value} onChange={handleInternalEdit} />;
        }
    };
    return (
        <TableCell colSpan={span}>
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
    value: PropTypes.any,
    index: PropTypes.number.isRequired,
    editIndex: PropTypes.number.isRequired,
    handleEdit: PropTypes.func.isRequired,
    type: PropTypes.string,
    options: PropTypes.array,
    span: PropTypes.number,
};
IngredientCell.defaultProps = {
    span: 1,
};
