import * as React from "react";
import Typography from "@mui/material/Typography";
import Title from "./Title";

export default function Deposits({ currentWatt, datetime }) {
  return (
    <React.Fragment>
      <Title>Current Power</Title>
      <Typography component="p" variant="h4">
        {currentWatt} W
      </Typography>
      <Typography color="text.secondary" sx={{ flex: 1 }}>
        {datetime}
      </Typography>
    </React.Fragment>
  );
}
