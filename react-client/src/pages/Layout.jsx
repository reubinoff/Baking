import React from "react";
import { Box } from "@mui/material";
import BakingNavBar from "../components/BakingNavBar";
import { Outlet } from "react-router-dom";

import {SearchContext} from "../components/context/SearchContext";

function Layout(props) {
  const [query, setQuery] = React.useState("");
    const [searchMode, setSearchMode] = React.useState(false);
    const contextValue = {
      query: query,
      setQuery: setQuery,
      searchMode: searchMode,
      setSearchMode: setSearchMode,
    };
  return (
    <Box sx={{ display: "flex" }}>
      <SearchContext.Provider value={contextValue}>
        <BakingNavBar searchMode={true}></BakingNavBar>
        <Box component="main" sx={{ pt: 9, pr: 2, pl: 2, width: 1 }}>
          <Outlet />
        </Box>
      </SearchContext.Provider>
    </Box>
  );
}

export default Layout;
