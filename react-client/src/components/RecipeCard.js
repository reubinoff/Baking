import React, { useCallback, useState } from "react";
import Button from "react-bootstrap/Button";
import Card from "react-bootstrap/Card";
import PropTypes from "prop-types";
import {
  IoWaterSharp,
  IoHeart,
  IoHeartOutline,
  IoShareSocialSharp,
} from "react-icons/io5";
import Col from "react-bootstrap/Col";
import Row from "react-bootstrap/Row";
import Badge from "react-bootstrap/Badge";
import Placeholder from "react-bootstrap/Placeholder";

export default function RecipeCard(props) {
  const [recipe] = useState(props.recipe);
  const [loading, setLoading] = useState(true);
  const [favorite, setFavorite] = useState(false);

  const changeFavorite = useCallback(() => {
    setFavorite(!favorite);
  }, [favorite]);

  const handleImageLoaded = useCallback(() => {
    setLoading(false);
  }, []);

  return (
    <Card>
      <Card.Header>{recipe.name}</Card.Header>
      <Card.Img variant="top" src={recipe.cdn_url} onLoad={handleImageLoaded} />
      {loading && <Card.Img variant="top" src="images/placeholder.png" />}
      {loading && (<Placeholder as={Card.Title} animation="glow">
          <Placeholder xs={6} />
        </Placeholder>)}

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
      <Card.Footer>
        <Button variant="" onClick={changeFavorite}>
          {favorite ? <IoHeartOutline color="red" /> : <IoHeart color="red" />}
        </Button>
        <Button variant="">
          <IoShareSocialSharp />
        </Button>
      </Card.Footer>
    </Card>
  );
}

RecipeCard.propTypes = {
  recipe: PropTypes.object.isRequired,
};
