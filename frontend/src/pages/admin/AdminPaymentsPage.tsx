import { Stack, Typography } from "@mui/material";

import { DataTable } from "@/components/common/DataTable";

export const AdminPaymentsPage = () => {
  const rows = [
    { id: 7001, order_id: 9001, amount: "INR 1900", status: "SUCCESS", gateway: "MOCK" },
    { id: 7002, order_id: 9002, amount: "INR 780", status: "PENDING", gateway: "MOCK" },
  ];

  return (
    <Stack spacing={2}>
      <Typography variant="h4" fontWeight={700}>
        Payment Monitoring
      </Typography>
      <DataTable
        columns={[
          { key: "id", label: "Payment ID" },
          { key: "order_id", label: "Order ID" },
          { key: "amount", label: "Amount" },
          { key: "status", label: "Status" },
          { key: "gateway", label: "Gateway" },
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

