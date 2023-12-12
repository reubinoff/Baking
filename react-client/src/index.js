import React from "react";
import ReactDOM from "react-dom/client";
import "./index.css";
import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
import reportWebVitals from "./reportWebVitals";
import { createTheme, ThemeProvider } from "@mui/material/styles";

import { QueryClient, QueryClientProvider } from "react-query";
import { Provider } from "react-redux";

import DefaultAppContextProvider from "./components/context/DefaultAppContextProvider";
import configureStore from "./configureStore";

const theme = createTheme({
  palette: {
    primary: {
      light: "#757ce8",
      main: "#e65100",
      dark: "#002884",
      contrastText: "#fff",
    },
    secondary: {
      light: "#ff7961",
      main: "#e65100",
      dark: "#ba000d",
      contrastText: "#000",
    },
  },
});

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      cacheTime: 600000, // 10 mins
    },
  },
});
const store = configureStore();
const root = ReactDOM.createRoot(document.getElementById("root"));
root.render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <Provider store={store}>
        <BrowserRouter>
          <DefaultAppContextProvider>
            <QueryClientProvider client={queryClient}>
              <App />
            </QueryClientProvider>
          </DefaultAppContextProvider>
        </BrowserRouter>
      </Provider>
    </ThemeProvider>
  </React.StrictMode>
);

if (process.env.NODE_ENV !== "production" && module.hot) {
  module.hot.accept("./components/App", root);
}

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
