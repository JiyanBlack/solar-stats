import Dashboard from "./components/Dashboard";
import * as React from "react";
import dayjs from "dayjs";
import utc from "dayjs/plugin/utc";
import timezone from "dayjs/plugin/timezone";

dayjs.extend(utc);
dayjs.extend(timezone);

// const serverUrl = "http://localhost:3000";
const serverUrl = "https://solarstats.tplinkdns.com";

function App() {
  const [wattData, setWattData] = React.useState([]);
  const [aggData, setAggData] = React.useState([]);

  React.useEffect(() => {
    const requestBody = {
      query_end_time: dayjs.utc().format(),
      query_start_time: dayjs.utc().subtract(3, "day").format(),
      gap: 60,
      intz: dayjs.tz.guess(),
    };
    fetch(serverUrl + "/api/get_watt_history")
      .then((response) => response.json())
      .then((data) => setWattData(data));
    fetch(serverUrl + "/api/get_aggregated_watt", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
      },
      body: JSON.stringify(requestBody),
    })
      .then((response) => response.json())
      .then((data) => setAggData(data));
  }, []);

  return (
    <Dashboard wattData={wattData} serverUrl={serverUrl} aggData={aggData} />
  );
}

export default App;
