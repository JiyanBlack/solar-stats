import * as React from "react";
import Typography from "@mui/material/Typography";
import Title from "./Title";
import dayjs from "dayjs";

export default function RealtimeBoard({ serverUrl }) {
  const [url] = React.useState(serverUrl);

  const [currentWatt, setCurrentWatt] = React.useState(0);
  const [datetime, setDatetime] = React.useState(
    dayjs().format("YYYY-MM-DD HH:mm:ss")
  );

  React.useEffect(() => {
    const interval = setInterval(() => {
      fetch(url + "/api/get_watt")
        .then((response) => response.json())
        .then((data) => setCurrentWatt(data.watt));
      setDatetime(dayjs().format("YYYY-MM-DD HH:mm:ss"));
    }, 1000);
    return () => clearInterval(interval);
  });

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
