import { useRef } from "react";
import SearchIcon from "@mui/icons-material/Search";
import { styled, alpha } from "@mui/material/styles";
import { useContext } from "react";
import { SearchContext } from "../components/context/SearchContext";
import Autocomplete from "@mui/material/Autocomplete";
import TextField from "@mui/material/TextField";
import PropTypes from "prop-types";


const Search = styled("div")(({ theme }) => ({
  position: "relative",
  borderRadius: theme.shape.borderRadius,
  backgroundColor: alpha(theme.palette.common.white, 0.15),
  "&:hover": {
    backgroundColor: alpha(theme.palette.common.white, 0.25),
  },
  marginLeft: 0,
  width: "100%",
  [theme.breakpoints.up("sm")]: {
    marginLeft: theme.spacing(1),
    width: "auto",
  },
}));

const SearchIconWrapper = styled("div")(({ theme }) => ({
  padding: theme.spacing(0, 2),
  height: "100%",
  position: "absolute",
  pointerEvents: "none",
  display: "flex",
  alignItems: "center",
  justifyContent: "center",
}));

const StyledAutocomplete = styled(Autocomplete)(({ theme }) => ({
  color: "inherit",
  width: "100%",
  "& .MuiAutocomplete-inputRoot": {
    padding: theme.spacing(1, 1, 1, 0),
    // vertical padding + font size from searchIcon
    paddingLeft: `calc(1em + ${theme.spacing(4)})`,
    transition: theme.transitions.create("width"),
    width: "100%",
    [theme.breakpoints.up("sm")]: {
      width: "30ch",
      "&:focus": {
        width: "70ch",
      },
    },
  },
}));

export default function BakingSearchBar(props) {
  const { setQuery } = useContext(SearchContext);
  const SearchRef = useRef(null);
  const onChange = (event, value) => {
    if (event?.type === "keydown" && event.key === "Enter") {
      return setQuery(value);
    }
    if (value === "") {
      setQuery(value);
    }
  };
  const InputChanged = (event, value) => {
    if (event?.type === "keydown" && event.key === "Enter") {
      return setQuery(event.target.value);
    } else if (event?.type === "click") {
      const val = value || "";
      return setQuery(val);
    } else if (event?.type === "change" && value === "") {
      return setQuery(value);
    }
  };

  return (
    <Search sx={{ display: props.show ? "flex" : "none" }}>
      <SearchIconWrapper>
        <SearchIcon />
      </SearchIconWrapper>
      <StyledAutocomplete
        freeSolo
        disableClearable
        onInputChange={InputChanged}
        onChange={onChange}
        id="baking-search"
        options={top100Films.map((option) => option.title)}
        renderInput={(params) => (
          <TextField
            ref={SearchRef}
            {...params}
            InputProps={{
              ...params.InputProps,
              type: "search",
            }}
          />
        )}
      />
    </Search>
  );
}

const top100Films = [
  { title: "fros", year: 1994 },
  { title: "track", year: 1972 },
  { title: "nokia", year: 1974 },
  { title: "no result option", year: 1974 },
];

BakingSearchBar.propTypes = {
  show: PropTypes.bool,
};
