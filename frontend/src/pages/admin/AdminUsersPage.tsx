import { Stack, Typography } from "@mui/material";

import { DataTable } from "@/components/common/DataTable";

export const AdminUsersPage = () => {
  const rows = [
    { id: 1, email: "customer@test.com", role: "customer" },
    { id: 2, email: "seller@test.com", role: "seller" },
  ];

  return (
    <Stack spacing={2}>
      <Typography variant="h4" fontWeight={700}>
        User Management
      </Typography>
      <DataTable
        columns={[
          { key: "id", label: "User ID" },
          { key: "email", label: "Email" },
          { key: "role", label: "Role" },
        ]}
        rows={rows}
        page={0}
        rowsPerPage={rows.length}
        total={rows.length}
        onPageChange={() => undefined}
      />
    </Stack>
  );
};

