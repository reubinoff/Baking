import * as React from "react";
import Box from "@mui/material/Box";
import Button from "@mui/material/Button";
import List from "@mui/material/List";
import Divider from "@mui/material/Divider";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemIcon from "@mui/material/ListItemIcon";
import ListItemText from "@mui/material/ListItemText";
import Home from "@mui/icons-material/Home";
import TuneIcon from "@mui/icons-material/Tune";
import FavoriteIcon from "@mui/icons-material/Favorite";
import InfoIcon from "@mui/icons-material/Info";
import PropTypes from "prop-types";
import { Link } from "react-router-dom";
import { Typography } from "@mui/material";
import Stack from "@mui/material/Stack";

export default function BakingDrawer({ setOpen }) {
  const toggleDrawer = (status) => (event) => {
    if (
      event &&
      event.type === "keydown" &&
      (event.key === "Tab" || event.key === "Shift")
    ) {
      return;
    }
    setOpen(status);
  };

  const items = [
    {
      text: "Home",
      icon: <Home />,
      to: "",
    },

    {
      text: "Favorites",
      icon: <FavoriteIcon />,
      to: "favorites",
    },
  ];
  const items2 = [
    {
      text: "settings",
      icon: <TuneIcon />,
      to: "settings",
    },
    {
      text: "about",
      icon: <InfoIcon />,
      to: "about",
    },
  ];
  const list = () => (
    <Box
      sx={{ width: 250 }}
      role="presentation"
      onClick={toggleDrawer(false)}
      onKeyDown={toggleDrawer(false)}
    >
      <List>
        {items.map((item, index) => (
          <ListItem disablePadding key={item.text}>
            <ListItemButton
              component={Link}
              to={item.to}
              selected={`/${item.to}` === window.location.pathname}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
      <Divider />
      <List>
        {items2.map((item, index) => (
          <ListItem disablePadding key={item.text}>
            <ListItemButton
              component={Link}
              to={item.to}
              selected={`/${item.to}` === window.location.pathname}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <React.Fragment>
      <Button onClick={toggleDrawer(true)} component={Link} to="">
        Baking
      </Button>
      {list()}
      {Footer()}
    </React.Fragment>
  );
}


function Footer() {
  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: "center",
        position: "absolute",
        pb: 2,
        bottom: 0,
      }}
    >
      <Stack>
        <Divider />

        <Typography sx={{ letterSpacing: 4 }} fontStyle={""}>
          made with
          <FavoriteIcon
            style={{ position: "relative", top: "8px" }}
            color="error"
          />
        </Typography>
        <Typography sx={{ letterSpacing: 4 }} fontStyle={"oblique"}>
          by Moshe Reubinoff
        </Typography>
      </Stack>
    </Box>
  );
}

BakingDrawer.propTypes = {
  setOpen: PropTypes.func,
};