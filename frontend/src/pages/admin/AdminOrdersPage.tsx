import { Stack, Typography } from "@mui/material";

import { DataTable } from "@/components/common/DataTable";

export const AdminOrdersPage = () => {
  const rows = [
    { id: 9001, user_id: 103, status: "PAID", total: "INR 1900" },
    { id: 9002, user_id: 105, status: "PENDING_PAYMENT", total: "INR 780" },
  ];

  return (
    <Stack spacing={2}>
      <Typography variant="h4" fontWeight={700}>
        Order Monitoring
      </Typography>
      <DataTable
        columns={[
          { key: "id", label: "Order ID" },
          { key: "user_id", label: "User ID" },
          { key: "status", label: "Status" },
          { key: "total", label: "Total" },
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

