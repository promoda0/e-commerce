import { Grid, Typography } from "@mui/material";

import { DashboardCard } from "@/components/dashboard/DashboardCard";

export const AdminDashboardPage = () => (
  <>
    <Typography variant="h4" fontWeight={700} gutterBottom>
      Admin Dashboard
    </Typography>
    <Grid container spacing={2}>
      <Grid item xs={12} md={3}>
        <DashboardCard title="Total Users" value={1245} />
      </Grid>
      <Grid item xs={12} md={3}>
        <DashboardCard title="Orders Today" value={132} />
      </Grid>
      <Grid item xs={12} md={3}>
        <DashboardCard title="Payments Success" value="96.2%" />
      </Grid>
      <Grid item xs={12} md={3}>
        <DashboardCard title="Low Inventory Alerts" value={11} />
      </Grid>
    </Grid>
  </>
);

