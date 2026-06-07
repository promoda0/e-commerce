import { Grid, Typography } from "@mui/material";

import { DashboardCard } from "@/components/dashboard/DashboardCard";

export const AdminAnalyticsPage = () => (
  <>
    <Typography variant="h4" fontWeight={700} gutterBottom>
      Analytics
    </Typography>
    <Grid container spacing={2}>
      <Grid item xs={12} md={4}>
        <DashboardCard title="GMV" value="INR 12.4L" subtitle="Last 30 days" />
      </Grid>
      <Grid item xs={12} md={4}>
        <DashboardCard title="Conversion Rate" value="3.9%" subtitle="Web traffic to checkout" />
      </Grid>
      <Grid item xs={12} md={4}>
        <DashboardCard title="Refund Rate" value="1.2%" subtitle="Healthy range" />
      </Grid>
    </Grid>
  </>
);

