import Col from "react-bootstrap/Col";
import PropTypes from "prop-types";
import React from "react";
import Row from "react-bootstrap/esm/Row";

export default function PlaceholderItems(props) {
  const { placeholder, total, ready } = props;

  return (
    <div>
      {!ready && (
        <Row xs={1} md={2} lg={3} className="g-4">
          {[...new Array(total).keys()].map((i) => (
            <Col key={i}>{React.createElement(placeholder, { key: i })}</Col>
          ))}
        </Row>
      )}
    </div>
  );
}

PlaceholderItems.propTypes = {
  placeholder: PropTypes.func.isRequired,
  total: PropTypes.number.isRequired,
  ready: PropTypes.bool.isRequired,
};

// defulat values
PlaceholderItems.defaultProps = {
  total: 5,
};
