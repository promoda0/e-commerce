import { Button, Stack, Typography } from "@mui/material";
import { Link } from "react-router-dom";

export const NotFoundPage = () => (
  <Stack spacing={2} alignItems="flex-start" p={4}>
    <Typography variant="h4" fontWeight={700}>
      404
    </Typography>
    <Typography variant="body1">The page you requested does not exist.</Typography>
    <Button component={Link} to="/" variant="contained">
      Go Home
    </Button>
  </Stack>
);

