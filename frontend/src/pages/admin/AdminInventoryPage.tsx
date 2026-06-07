import { Stack, Typography } from "@mui/material";

import { DataTable } from "@/components/common/DataTable";

export const AdminInventoryPage = () => {
  const rows = [
    { product_id: 1, available_stock: 15, reserved_stock: 4, reorder_level: 10, is_low_stock: false },
    { product_id: 2, available_stock: 5, reserved_stock: 3, reorder_level: 8, is_low_stock: true },
  ];

  return (
    <Stack spacing={2}>
      <Typography variant="h4" fontWeight={700}>
        Inventory Monitoring
      </Typography>
      <DataTable
        columns={[
          { key: "product_id", label: "Product ID" },
          { key: "available_stock", label: "Available" },
          { key: "reserved_stock", label: "Reserved" },
          { key: "reorder_level", label: "Reorder Level" },
          { key: "is_low_stock", label: "Low Stock" },
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

