import React from "react";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import RecipeCard from "./RecipeCard";
import PropTypes from "prop-types";


class RecipeGrid extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      recipes: this.props.recipes,
    };
  }

  render() {
    const { recipes, loading } = this.state;

    if (loading) {
      return <div>Loading...</div>;
    }
    
    return (
      <Row xs={1} md={4} className="g-4">
        {recipes.map((recipe) => (
        <Col key={recipe.id}>
          <RecipeCard recipe={recipe} />
        
        </Col>
        ))}
      </Row>
      );
    }
  }

RecipeGrid.propTypes = {
  recipes: PropTypes.array.isRequired,
};

export default RecipeGrid;
