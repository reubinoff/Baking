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
import Spinner from "react-bootstrap/esm/Spinner";

class RecipeCard extends Component {
  constructor(recipe) {
    super(recipe);
    this.state = {
      recipe: this.props.recipe,
      imageLoading: true,
    };
  }

  changeFavorite() {
    // console.log("changeFavorite");
    this.setState({
      recipe: {
        ...this.state.recipe,
        favorite: !this.state.recipe.favorite,
      },
    });
  }

  handleImageLoaded() {
    console.log("handleImageLoaded");
    this.setState({ imageLoading: false });
  }

  render() {
    const { recipe, imageLoading } = this.state;
    return (
      <Card>
        <Card.Header>{recipe.name}</Card.Header>
        <Card.Img
          
          variant="top"
          src={recipe.cdn_url}
          onLoad={this.handleImageLoaded.bind(this)}
        />
        {imageLoading && <Spinner animation="border" role="status" />}

        <Card.Body>
          <Row>
            <Col xs={7} sm={8}>
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

  {/*

  final List<Procedure> procedures; */}