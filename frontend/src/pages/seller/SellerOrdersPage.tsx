import { Stack, Typography } from "@mui/material";

import { DataTable } from "@/components/common/DataTable";

export const SellerOrdersPage = () => {
  const rows = [
    { id: 101, customer: "User 1", status: "PROCESSING", total: "INR 2400" },
    { id: 102, customer: "User 2", status: "SHIPPED", total: "INR 1800" },
  ];

  return (
    <Stack spacing={2}>
      <Typography variant="h4" fontWeight={700}>
        Seller Order Management
      </Typography>
      <DataTable
        columns={[
          { key: "id", label: "Order ID" },
          { key: "customer", label: "Customer" },
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

