import React, {Component} from "react";
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import PropTypes from 'prop-types';


class RecipeCard extends Component {
  constructor(recipe) {
    super(recipe);
    this.state = {
      recipe: this.props.recipe
    };
  }



  render() {
    const {recipe} = this.state;
    return (
     <Card >
      <Card.Img variant="top" src="images/bread_placeholder.jpeg" />
      <Card.Body>
        <Card.Title>{recipe.name}</Card.Title>
        <Card.Text>{recipe.description}</Card.Text>
      </Card.Body>
      <Card.Footer >
        <Button variant="warning">Go somewhere</Button>
      </Card.Footer>
    </Card>
    );
  }
}

RecipeCard.propTypes = {
  recipe: PropTypes.object.isRequired
}
export default RecipeCard;

  {/* final String name;
  final String description;
  final int id;
  final int hydration;
  final String? imageUrl;
  final String? cdnUrl;
  final List<Procedure> procedures; */}