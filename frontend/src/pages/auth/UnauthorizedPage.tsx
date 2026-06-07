import { Alert, Typography } from "@mui/material";

export const UnauthorizedPage = () => (
  <>
    <Typography variant="h5" fontWeight={700} gutterBottom>
      Unauthorized
    </Typography>
    <Alert severity="warning">You need to login to access this page.</Alert>
  </>
);

