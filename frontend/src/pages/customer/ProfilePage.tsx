import { Card, CardContent, Stack, Typography } from "@mui/material";

import { useAuth } from "@/store/AuthContext";

export const ProfilePage = () => {
  const { user } = useAuth();

  return (
    <Card>
      <CardContent>
        <Stack spacing={1}>
          <Typography variant="h4" fontWeight={700}>
            Profile
          </Typography>
          <Typography>User ID: {user?.id ?? "-"}</Typography>
          <Typography>Role: {user?.role ?? "-"}</Typography>
        </Stack>
      </CardContent>
    </Card>
  );
};

