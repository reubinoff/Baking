import React, {Component} from "react";
import Button from 'react-bootstrap/Button';
import Card from 'react-bootstrap/Card';
import PropTypes from 'prop-types';
import {
  IoWaterSharp,
  IoHeart,
  IoHeartOutline,
  IoShareSocialSharp,
} from "react-icons/io5";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Badge from "react-bootstrap/Badge";

class RecipeCard extends Component {
  constructor(recipe) {
    super(recipe);
    this.state = {
      recipe: this.props.recipe
    };
  }

  changeFavorite() {
    // console.log("changeFavorite");
    this.setState({
      recipe: {
        ...this.state.recipe,
        favorite: !this.state.recipe.favorite
      }
    });
  }

  render() {
    const {recipe} = this.state;
    return (
      <Card>
        {/* <Card.Img variant="top" src="images/bread_placeholder.jpeg" /> */}
        <Card.Img variant="top" src={recipe.cdn_url} />
        <Card.Body>
          <Row>
            <Col>
              <Card.Title>{recipe.name}</Card.Title>
              <Card.Text>{recipe.description}</Card.Text>
            </Col>
            <Col>
              <div style={{ display: "flex", justifyContent: "flex-end" }}>
                <IoWaterSharp color="blue" />
                <Badge pill bg="light" text="dark">
                  {recipe.hydration}%
                </Badge>
              </div>
            </Col>
          </Row>
        </Card.Body>
        {this.get_footer()}
      </Card>
    );
  }

  get_footer() {
    return (
      <Card.Footer>
        <Button variant="" onClick={() => this.changeFavorite()}>
          {this.state.recipe.favorite ? (
            <IoHeartOutline color="red" />
          ) : (
            <IoHeart color="red" />
          )}
        </Button>
        <Button variant="">
          <IoShareSocialSharp />
        </Button>
      </Card.Footer>
    );

  }
}

RecipeCard.propTypes = {
  recipe: PropTypes.object.isRequired
}
export default RecipeCard;

  {/* final String name;
  final String? imageUrl;
  final String? cdnUrl;
  final List<Procedure> procedures; */}