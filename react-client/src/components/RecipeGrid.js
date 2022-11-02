import React from "react";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import RecipeCard from "./RecipeCard";
import PropTypes from "prop-types";
import Spinner from "react-bootstrap/Spinner";

class RecipeGrid extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      recipes: this.props.recipes,
      loading: true,
    };
  }

  // featch data
  componentDidMount() {
    this.setState({ loading: true });
    fetch("http://localhost:8888/recipe?page=1&itemsPerPage=10")
      .then((response) => response.json())
      .then((data) => this.setState({ recipes: data.items, loading: false }));
  }

  render() {
    const { loading, recipes } = this.state;

    if (loading) {
      return (
        <div className="d-flex align-items-center">
          <Spinner animation="border" role="status" size="xxl" className="mr-2">
            <span className="visually-hidden">Loading...</span>
          </Spinner>
        </div>
      );
    } else {
      return (
        <Row xs={1} md={2} lg={4} className="g-4">
          {recipes.map((recipe) => (
            <Col key={recipe.id}>
              <RecipeCard recipe={recipe} />
            </Col>
          ))}
        </Row>
      );
    }
  }
}

RecipeGrid.propTypes = {
  recipes: PropTypes.array.isRequired,
};

export default RecipeGrid;
