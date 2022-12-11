import * as React from "react";
import Box from "@mui/material/Box";
import { DataGrid } from "@mui/x-data-grid";
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import timezone from "dayjs/plugin/timezone";
import localizedFormat from "dayjs/plugin/localizedFormat";
dayjs.extend(localizedFormat);
dayjs.extend(utc);
dayjs.extend(timezone);

const columns = [
  {
    field: "watt",
    headerName: "Power(watt)",
    width: 110,
  },
  {
    field: "ts",
    headerName: "Timestamp",
    width: 200,
  },
  { field: "id", headerName: "ID", width: 80 },
];

export default function TableRecords({ wattData }) {
  const tz = dayjs.tz.guess();
  const wattDataTimestampProcessed = wattData.map((d) => ({
    ...d,
    ts: dayjs(d.ts).tz(tz).format("lll"),
  }));
  return (
    <Box sx={{ height: 640, width: "100%" }}>
      <DataGrid
        rows={wattDataTimestampProcessed}
        columns={columns}
        pageSize={10}
        rowsPerPageOptions={[10]}
        disableSelectionOnClick
        experimentalFeatures={{ newEditingApi: true }}
      />
    </Box>
  );
}
