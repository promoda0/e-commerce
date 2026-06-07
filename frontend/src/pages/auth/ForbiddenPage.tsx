import { Alert, Typography } from "@mui/material";

export const ForbiddenPage = () => (
  <>
    <Typography variant="h5" fontWeight={700} gutterBottom>
      Forbidden
    </Typography>
    <Alert severity="error">You do not have permission to access this page.</Alert>
  </>
);

