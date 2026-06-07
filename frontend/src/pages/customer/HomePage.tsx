import { Grid, Typography } from "@mui/material";

import { DashboardCard } from "@/components/dashboard/DashboardCard";

export const HomePage = () => (
  <>
    <Typography variant="h4" fontWeight={700} gutterBottom>
      Customer Home
    </Typography>
    <Grid container spacing={2}>
      <Grid item xs={12} md={4}>
        <DashboardCard title="Featured Products" value={24} subtitle="Curated for you" />
      </Grid>
      <Grid item xs={12} md={4}>
        <DashboardCard title="Active Orders" value={3} subtitle="In progress" />
      </Grid>
      <Grid item xs={12} md={4}>
        <DashboardCard title="Saved Amount" value="INR 1,250" subtitle="This month" />
      </Grid>
    </Grid>
  </>
);

