import {
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TablePagination,
  TableRow,
  Typography,
} from "@mui/material";

interface Column<T> {
  key: keyof T;
  label: string;
}

interface DataTableProps<T extends Record<string, unknown>> {
  columns: Column<T>[];
  rows: T[];
  page: number;
  rowsPerPage: number;
  total: number;
  onPageChange: (page: number) => void;
}

export const DataTable = <T extends Record<string, unknown>>({
  columns,
  rows,
  page,
  rowsPerPage,
  total,
  onPageChange,
}: DataTableProps<T>) => {
  return (
    <Paper>
      <TableContainer>
        <Table size="small">
          <TableHead>
            <TableRow>
              {columns.map((column) => (
                <TableCell key={String(column.key)}>{column.label}</TableCell>
              ))}
            </TableRow>
          </TableHead>
          <TableBody>
            {rows.length === 0 ? (
              <TableRow>
                <TableCell colSpan={columns.length}>
                  <Typography variant="body2" color="text.secondary">
                    No records available
                  </Typography>
                </TableCell>
              </TableRow>
            ) : (
              rows.map((row, index) => (
                <TableRow key={index}>
                  {columns.map((column) => (
                    <TableCell key={String(column.key)}>{String(row[column.key] ?? "-")}</TableCell>
                  ))}
                </TableRow>
              ))
            )}
          </TableBody>
        </Table>
      </TableContainer>
      <TablePagination
        component="div"
        rowsPerPageOptions={[rowsPerPage]}
        page={page}
        onPageChange={(_, newPage) => onPageChange(newPage)}
        rowsPerPage={rowsPerPage}
        count={total}
      />
    </Paper>
  );
};

