import React from "react";
import useDocumentTitle from "../hooks/useDocumentTitle";
import PropTypes from "prop-types";

export default function Page(props) {
    const {title, content} = props;
  const titlePrefix = "AppName 🤠 | ";
  useDocumentTitle(`${titlePrefix}${title}`);
  return <React.Fragment>{content}</React.Fragment>;
}

Page.propTypes = {
    title: PropTypes.string.isRequired,
    content: PropTypes.string.isRequired,
};