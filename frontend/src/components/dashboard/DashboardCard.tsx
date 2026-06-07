import { Card, CardContent, Typography } from "@mui/material";

interface DashboardCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
}

export const DashboardCard = ({ title, value, subtitle }: DashboardCardProps) => (
  <Card>
    <CardContent>
      <Typography variant="body2" color="text.secondary">
        {title}
      </Typography>
      <Typography variant="h5" fontWeight={700}>
        {value}
      </Typography>
      {subtitle ? (
        <Typography variant="caption" color="text.secondary">
          {subtitle}
        </Typography>
      ) : null}
    </CardContent>
  </Card>
);

