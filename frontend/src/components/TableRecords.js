import * as React from "react";
import Box from "@mui/material/Box";
import { DataGrid } from "@mui/x-data-grid";

const columns = [
  { field: "id", headerName: "ID", width: 80 },
  {
    field: "ts",
    headerName: "Timestamp",
    width: 300,
  },
  {
    field: "watt",
    headerName: "Power(watt)",
    width: 110,
  },
];

export default function TableRecords({ wattData }) {
  return (
    <Box sx={{ height: 640, width: "100%" }}>
      <DataGrid
        rows={wattData}
        columns={columns}
        pageSize={10}
        rowsPerPageOptions={[10]}
        disableSelectionOnClick
        experimentalFeatures={{ newEditingApi: true }}
      />
    </Box>
  );
}
