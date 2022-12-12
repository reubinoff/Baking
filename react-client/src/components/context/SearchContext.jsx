import { createContext } from "react";

export const SearchContext = createContext({
  query: "",
  setQuery: () => {},
  searchMode: false,
  setSearchMode: () => {},
});
