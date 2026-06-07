import { Box, Container, Paper } from "@mui/material";
import { Outlet } from "react-router-dom";

export const AuthLayout = () => (
  <Container maxWidth="sm" sx={{ minHeight: "100vh", display: "flex", alignItems: "center" }}>
    <Paper elevation={3} sx={{ width: "100%", p: 4 }}>
      <Outlet />
    </Paper>
  </Container>
);

