import json

import requests


class FroniusConnector:
    """
    Connector connects Fronius Inverter API v1 to Python Objects
    """

    def __init__(self, ipaddress):
        self.ip = ipaddress  # LAN IP address of Fronius Inverter

    def request_api_version(self):
        return "http://{}/solar_api/GetAPIVersion.cgi".format(self.ip), {}

    def request_get_system_realtime_data(self):
        return "http://{}/solar_api/v1/GetInverterRealtimeData.cgi".format(self.ip), {"Scope": "System"}

    def request_logger_data(self):
        return "http://{}/solar_api/v1/GetLoggerInfo.cgi".format(self.ip), {}

    def request_historic_data(self, start, end, series_type):
        print("Fetch {} data of EnergyReal_WAC_Sum_Produced for date period {} to {}".format(series_type, start, end))
        return (
            "http://{}/solar_api/v1/GetArchiveData.cgi".format(self.ip),
            {
                "Scope": "System",
                "SeriesType": series_type,
                "StartDate": start,
                "EndDate": end,
                "Channel": "EnergyReal_WAC_Sum_Produced",
            },
        )

    def fetch_realtime_watt(self, timeout=5):
        url, params = self.request_get_system_realtime_data()
        r = requests.get(url, params=params, timeout=timeout)
        res = json.loads(r.text)
        return res["Body"]["Data"]["PAC"]["Values"]["1"]


def main():
    fc = FroniusConnector("192.168.0.227")
    print(fc.fetch_realtime_watt())


if __name__ == "__main__":
    main()
