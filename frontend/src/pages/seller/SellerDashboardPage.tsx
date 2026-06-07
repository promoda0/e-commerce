import { Grid, Typography } from "@mui/material";

import { DashboardCard } from "@/components/dashboard/DashboardCard";

export const SellerDashboardPage = () => (
  <>
    <Typography variant="h4" fontWeight={700} gutterBottom>
      Seller Dashboard
    </Typography>
    <Grid container spacing={2}>
      <Grid item xs={12} md={4}>
        <DashboardCard title="Total Products" value={48} />
      </Grid>
      <Grid item xs={12} md={4}>
        <DashboardCard title="Open Orders" value={12} />
      </Grid>
      <Grid item xs={12} md={4}>
        <DashboardCard title="Low Stock Alerts" value={4} />
      </Grid>
    </Grid>
  </>
);

