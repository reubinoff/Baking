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
import Drawer from "@mui/material/Drawer";
import BakingSearchBar from "./BakingSearchBar";
import HideOnScroll from "./HideOnScroll";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import { useLocation } from "react-router-dom";
import { useNavigate } from "react-router-dom";
import { useContext } from "react";
import { SearchContext } from "../components/context/SearchContext";
import _ from "lodash";

export default function BakingNavBar(props) {
  const [, setAnchorElUser] = React.useState(null);
  const [open, setOpen] = React.useState(false);
  let location = useLocation();
  const navigate = useNavigate();
  const { query, setQuery } = useContext(SearchContext);


  const navHome = React.useCallback(() => {
    navigate("/");
    setQuery("");
  }, [navigate, setQuery]);


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
    if (isHome) {
      setQuery("");
    }
  }, [isHome, setQuery]);
  // const handleCloseUserMenu = () => {
  //   setAnchorElUser(null);
  // };
  const ShowBackButton = React.useMemo(() => {
    if (false === _.isEmpty(query)) {
      return true;
    }
    return !isHome;
  }, [isHome, query]);

  const ShowMenuButton = React.useMemo(() => !ShowBackButton, [ShowBackButton]);
  return (
    <HideOnScroll {...props}>
      <Box>
        <AppBar component="nav" enableColorOnDark>
          <Toolbar>
            <IconButton
              size="large"
              edge="start"
              color="inherit"
              aria-label="open drawer"
              onClick={navHome}
              sx={{
                mr: 2,
                display: ShowBackButton ? "flex" : "none",
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
                display: ShowMenuButton ? "flex" : "none",
              }}
            >
              <MenuIcon />
            </IconButton>
            <Typography
              variant="h6"
              noWrap
              component="div"
              sx={{ display: { xs: "none", sm: "flex" } }}
            >
              Baking
            </Typography>

            <Box flexDirection="row" sx={{ ml: "auto", display: "flex" }}>
              <BakingSearchBar show={isHome} />
              <Tooltip title="Open settings" >
                <IconButton onClick={handleOpenUserMenu} sx={{ p: 0 , ml: 2}}>
                  <Avatar
                    alt="Moshe Reubinoff"
                    src="https://i.pravatar.cc/300"
                  />
                </IconButton>
              </Tooltip>
            </Box>
          </Toolbar>
          <Drawer
            anchor="left"
            open={open}
            onOpen={toggleDrawer(true)}
            onClose={toggleDrawer(false)}
          >
            <BakingDrawer setOpen={toggleDrawer(false)}></BakingDrawer>
          </Drawer>
        </AppBar>
      </Box>
    </HideOnScroll>
  );
}

