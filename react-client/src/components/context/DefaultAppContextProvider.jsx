import handleError from "../../utils/handleError";
import AppContext from "./AppContext";

const BASE_URL = process.env.REACT_APP_BASE_URL;


export default function DefaultAppContextProvider({ ...props }) {
  return (
    <AppContext.Provider
      value={{
        ready: true,
        query: "",
        customTypeRenderers: {},
        customExecutionSummaryRows: [],
        customTaskSummaryRows: [],
        fetchWithContext: function (path, fetchParams) {
          const newParams = { ...fetchParams };

          const newPath = `${BASE_URL}/${path}`;
          const cleanPath = newPath.replace(/([^:]\/)\/+/g, "$1"); // Cleanup duplicated slashes

          return fetch(cleanPath, newParams).then(handleError);
        },
      }}
      {...props}
    />
  );
}
