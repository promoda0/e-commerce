import { Stack, Typography } from "@mui/material";

import { DataTable } from "@/components/common/DataTable";

export const SellerProductsPage = () => {
  const rows = [
    { id: 1, name: "Sample Product", status: "active", price: "INR 1200" },
    { id: 2, name: "Sample Product 2", status: "draft", price: "INR 850" },
  ];

  return (
    <Stack spacing={2}>
      <Typography variant="h4" fontWeight={700}>
        Seller Product Management
      </Typography>
      <DataTable
        columns={[
          { key: "id", label: "ID" },
          { key: "name", label: "Name" },
          { key: "status", label: "Status" },
          { key: "price", label: "Price" },
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

