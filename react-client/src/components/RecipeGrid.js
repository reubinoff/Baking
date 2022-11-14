import React from "react";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import RecipeCard from "./RecipeCard";
import Placeholder from "react-bootstrap/Placeholder";
import { getRecipes } from "../services/recipes";
import Card from "react-bootstrap/Card";

class RecipeGrid extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      recipes: [],
      loading: true,
    };
  }

  // featch data
  componentDidMount() {
    this.setState({ loading: true });
    getRecipes(1, 10)
      .then( (data) => this.setState({ recipes: data.items, loading: false }));
  }

  render() {
    const { loading, recipes } = this.state;

    if (loading) {
      return (
        <Row xs={1} md={2} lg={4} className="g-4">
          {[...Array(10).keys()].map((i) => (
            <Col key={i}>
              <Card >
                <Card.Img variant="top" src="images/placeholder.png" />
                <Card.Body>
                  <Placeholder as={Card.Title} animation="glow">
                    <Placeholder xs={6} />
                  </Placeholder>
                  <Placeholder as={Card.Text} animation="glow">
                    <Placeholder xs={7} /> <Placeholder xs={4} />{" "}
                    <Placeholder xs={4} /> <Placeholder xs={6} />{" "}
                    <Placeholder xs={8} />
                  </Placeholder>
                </Card.Body>
              </Card>
            </Col>
          ))}
        </Row>
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


export default RecipeGrid;
