import { Alert, Stack, Typography } from "@mui/material";

export const SellerInventoryPage = () => (
  <Stack spacing={2}>
    <Typography variant="h4" fontWeight={700}>
      Seller Inventory Management
    </Typography>
    <Alert severity="info">Inventory table, reserve/release actions, and low-stock badges can be wired here.</Alert>
  </Stack>
);

