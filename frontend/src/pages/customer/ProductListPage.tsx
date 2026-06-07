import SearchIcon from "@mui/icons-material/Search";
import { Box, CircularProgress, IconButton, InputAdornment, Paper, Stack, TextField, Typography } from "@mui/material";
import { useMemo, useState } from "react";
import { Link } from "react-router-dom";

import { DataTable } from "@/components/common/DataTable";
import { useProducts } from "@/hooks/useProducts";

export const ProductListPage = () => {
  const { data = [], isLoading } = useProducts();
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(0);
  const pageSize = 10;

  const filtered = useMemo(
    () =>
      data.filter((item) =>
        item.name.toLowerCase().includes(search.toLowerCase()) ||
        (item.category ?? "").toLowerCase().includes(search.toLowerCase()),
      ),
    [data, search],
  );

  const paged = filtered.slice(page * pageSize, page * pageSize + pageSize).map((item) => ({
    id: item.id,
    name: item.name,
    category: item.category ?? "-",
    price: `INR ${item.price}`,
    details: "View",
  }));

  return (
    <Stack spacing={2}>
      <Typography variant="h4" fontWeight={700}>
        Products
      </Typography>
      <TextField
        placeholder="Search by product or category"
        value={search}
        onChange={(event) => setSearch(event.target.value)}
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <IconButton>
                <SearchIcon />
              </IconButton>
            </InputAdornment>
          ),
        }}
      />
      {isLoading ? (
        <Box display="flex" justifyContent="center" py={4}>
          <CircularProgress />
        </Box>
      ) : (
        <Paper>
          <DataTable
            columns={[
              { key: "id", label: "ID" },
              { key: "name", label: "Name" },
              { key: "category", label: "Category" },
              { key: "price", label: "Price" },
              { key: "details", label: "Details" },
            ]}
            rows={paged}
            page={page}
            rowsPerPage={pageSize}
            total={filtered.length}
            onPageChange={setPage}
          />
        </Paper>
      )}
      <Typography variant="caption" color="text.secondary">
        Click any product row id and open `/products/:id` route for details.
      </Typography>
      <Typography component={Link} to="/products/1">
        Open sample details page
      </Typography>
    </Stack>
  );
};

