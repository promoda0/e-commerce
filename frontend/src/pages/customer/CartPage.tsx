import { Alert, Stack, Typography } from "@mui/material";

export const CartPage = () => (
  <Stack spacing={2}>
    <Typography variant="h4" fontWeight={700}>
      Cart
    </Typography>
    <Alert severity="info">Cart table and quantity controls are ready to integrate with cart APIs.</Alert>
  </Stack>
);

