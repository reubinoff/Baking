
import { PropTypes } from 'prop-types';

import { Box } from '@mui/material';
import {Paper} from '@mui/material';
import Typography from '@mui/material/Typography';
import RecipeIngridients from './RecipeIngridients';
import RecipeProcedure from './RecipeProcedure';
export default function RecipeView(props) {

    return (
      <Box>
        <h1>{props.recipe.name}</h1>
        <p>{props.recipe.description}</p>
        <Paper>
          <Typography variant="h6">
            Ingredients
            <RecipeIngridients ingredients={props.recipe.ingredients} />
          </Typography>
        </Paper>
        
        <Paper sx={{mt: 5}}>
          <Typography variant="h6">
            Procedures
            {props.recipe.procedures.map((procedure) => (
              <RecipeProcedure key={procedure.name} procedure={procedure} />
            ))}
          </Typography>
        </Paper>
      </Box>
    );

}


RecipeView.propTypes = {
  recipe: PropTypes.object.isRequired,
  req_hyration: PropTypes.number, // undefined for same as recipe
  req_total_loaf_weight: PropTypes.number, // undefined for same as recipe
  req_total_loaf_count: PropTypes.number, // undefined for same as recipe
};
