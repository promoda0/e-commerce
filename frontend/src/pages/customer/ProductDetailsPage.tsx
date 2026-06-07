import { Alert, Card, CardContent, CircularProgress, Stack, Typography } from "@mui/material";
import { useParams } from "react-router-dom";

import { useProduct } from "@/hooks/useProducts";

export const ProductDetailsPage = () => {
  const { productId = "" } = useParams();
  const { data, isLoading, isError } = useProduct(productId);

  if (isLoading) {
    return <CircularProgress />;
  }

  if (isError || !data) {
    return <Alert severity="error">Unable to load product details.</Alert>;
  }

  return (
    <Card>
      <CardContent>
        <Stack spacing={1}>
          <Typography variant="h4" fontWeight={700}>
            {data.name}
          </Typography>
          <Typography variant="body1">{data.description ?? "No description"}</Typography>
          <Typography variant="body2" color="text.secondary">
            Category: {data.category ?? "-"}
          </Typography>
          <Typography variant="h6">INR {data.price}</Typography>
          <Typography variant="caption">Stock: {data.stock_quantity}</Typography>
        </Stack>
      </CardContent>
    </Card>
  );
};

