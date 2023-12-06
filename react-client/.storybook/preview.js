/** @type { import('@storybook/react').Preview } */
import "@fontsource/roboto/300.css";
import "@fontsource/roboto/400.css";
import "@fontsource/roboto/500.css";
import "@fontsource/roboto/700.css";
// import "@fontsource/material-icons";
import { CssBaseline, ThemeProvider } from "@mui/material";
import { withThemeFromJSXProvider } from "@storybook/addon-themes";
// import { lightTheme, darkTheme } from "../src/themes.js";
import "../src/App.css";

const preview = {
  parameters: {
    actions: { argTypesRegex: "^on[A-Z].*" },
    controls: {
      matchers: {
        color: /(background|color)$/i,
        date: /Date$/i,
      },
    },
  },
};

export default preview;
