import React from "react";
import AppBar from "@mui/material/AppBar";
import Toolbar from "@mui/material/Toolbar";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";
import MenuIcon from "@mui/icons-material/Menu";

import Box from "@mui/material/Box";
import Tooltip from "@mui/material/Tooltip";
import Avatar from "@mui/material/Avatar";
import BakingDrawer from "./BakingDrawer";
import SwipeableDrawer from "@mui/material/SwipeableDrawer";
import BakingSearchBar from "./BakingSearchBar";
import HideOnScroll from "./HideOnScroll";
import PropTypes from "prop-types";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import { useLocation } from "react-router-dom";
import { useNavigate } from "react-router-dom";

export default function BakingNavBar(props) {
  const [, setAnchorElUser] = React.useState(null);
  const [open, setOpen] = React.useState(false);
  let location = useLocation();
  const navigate = useNavigate();
  const nav = (path) => (event) => {
    navigate(path);
  };

  const toggleDrawer = (open) => (event) => {
    if (
      event &&
      event.type === "keydown" &&
      (event.key === "Tab" || event.key === "Shift")
    ) {
      return;
    }

    setOpen(open);
  };

  const handleOpenUserMenu = (event) => {
    setAnchorElUser(event.currentTarget);
  };

  const isHome = React.useMemo(() => {
    return location.pathname === "/";
  }, [location]);
  React.useEffect(() => {
    if (isHome === true) {
      navigate("/");
    }
  }, [isHome, navigate]);
  // const handleCloseUserMenu = () => {
  //   setAnchorElUser(null);
  // };

  return (
    <HideOnScroll {...props}>
      <AppBar component="nav" enableColorOnDark>
        <Toolbar>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="open drawer"
            onClick={nav("/")}
            sx={{
              mr: 2,
              display: !isHome ? "block" : "none",
            }}
          >
            <ArrowBackIcon />
          </IconButton>
          <IconButton
            size="large"
            edge="start"
            color="inherit"
            aria-label="open drawer"
            onClick={toggleDrawer(true)}
            onKeyDown={toggleDrawer(false)}
            sx={{
              mr: 2,
              display: isHome ? "block" : "none",
            }}
          >
            <MenuIcon />
          </IconButton>
          <Typography
            variant="h6"
            noWrap
            component="div"
            sx={{ flexGrow: 1, display: { xs: "none", sm: "block" } }}
          >
            Baking
          </Typography>
          <BakingSearchBar setQuery={props.setQuery} />

          <Box sx={{ flexGrow: 0, ml: 2 }}>
            <Tooltip title="Open settings">
              <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 }}>
                <Avatar alt="Moshe Reubinoff" src="https://i.pravatar.cc/300" />
              </IconButton>
            </Tooltip>
          </Box>
        </Toolbar>
        <SwipeableDrawer
          anchor="left"
          open={open}
          onOpen={toggleDrawer(true)}
          onClose={toggleDrawer(false)}
        >
          <BakingDrawer setOpen={toggleDrawer(false)}></BakingDrawer>
        </SwipeableDrawer>
      </AppBar>
    </HideOnScroll>
  );
}

BakingNavBar.propTypes = {
  setQuery: PropTypes.func.isRequired,
};
