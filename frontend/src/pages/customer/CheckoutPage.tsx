import { Alert, Button, Stack, Typography } from "@mui/material";

export const CheckoutPage = () => (
  <Stack spacing={2}>
    <Typography variant="h4" fontWeight={700}>
      Checkout
    </Typography>
    <Alert severity="info">Connect this page with order creation and payment initiation APIs.</Alert>
    <Button variant="contained">Place Order</Button>
  </Stack>
);

