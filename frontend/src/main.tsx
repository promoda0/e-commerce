import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { CssBaseline, ThemeProvider, createTheme } from "@mui/material";

import App from "@/App";
import { AuthProvider } from "@/store/AuthContext";

const queryClient = new QueryClient();

const theme = createTheme({
  palette: {
    mode: "light",
    primary: {
      main: "#1565c0",
    },
    secondary: {
      main: "#00897b",
    },
  },
  shape: {
    borderRadius: 10,
  },
});

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          <BrowserRouter>
            <App />
          </BrowserRouter>
        </AuthProvider>
      </QueryClientProvider>
    </ThemeProvider>
  </React.StrictMode>,
);

