import { CircularProgress, Stack, Typography } from "@mui/material";

import { DataTable } from "@/components/common/DataTable";
import { useOrders } from "@/hooks/useOrders";

export const OrdersPage = () => {
  const { data = [], isLoading } = useOrders();

  if (isLoading) {
    return <CircularProgress />;
  }

  const rows = data.map((order) => ({
    id: order.id,
    status: order.status,
    amount: `INR ${order.total_amount}`,
    created_at: new Date(order.created_at).toLocaleString(),
  }));

  return (
    <Stack spacing={2}>
      <Typography variant="h4" fontWeight={700}>
        Orders
      </Typography>
      <DataTable
        columns={[
          { key: "id", label: "Order ID" },
          { key: "status", label: "Status" },
          { key: "amount", label: "Amount" },
          { key: "created_at", label: "Created At" },
        ]}
        rows={rows}
        page={0}
        rowsPerPage={Math.max(rows.length, 1)}
        total={rows.length}
        onPageChange={() => undefined}
      />
    </Stack>
  );
};

