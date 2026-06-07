import { Stack, Typography } from "@mui/material";

import { DataTable } from "@/components/common/DataTable";

export const AdminProductsPage = () => {
  const rows = [
    { id: 1, name: "Gaming Mouse", seller: 22, active: true },
    { id: 2, name: "Mechanical Keyboard", seller: 22, active: true },
  ];

  return (
    <Stack spacing={2}>
      <Typography variant="h4" fontWeight={700}>
        Product Monitoring
      </Typography>
      <DataTable
        columns={[
          { key: "id", label: "Product ID" },
          { key: "name", label: "Name" },
          { key: "seller", label: "Seller ID" },
          { key: "active", label: "Active" },
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

