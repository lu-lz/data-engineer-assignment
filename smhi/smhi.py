import argparse
import requests
import pandas as pd

class SmhiParser:
    """
    Class to handle communication with and extract data from the SMHI Open API.
    """
    VERSION = "1.0"
    BASE_URL = f"https://opendata-download-metobs.smhi.se/api/version/{VERSION}"

    def __init__(self, suffix=".json"):
        self.suffix = suffix

    def make_request(self, path=""):
        r = requests.get(self.BASE_URL+path+self.suffix)
        return r

def calculate_high_low_temperature(smhi_parser):
    highest_temp = -1000
    lowest_temp = 1000
    highest_place = ""
    lowest_place = ""
    path = "/parameter/2"
    response_station = smhi_parser.make_request(path=path)

    if response_station.status_code == 200:
        for el in response_station.json()["station"]:
            if el["active"] == True:
                response_temp = smhi_parser.make_request(path=f"{path}/station/{el['key']}/period/latest-day/data")
                if response_temp.status_code == 200:
                    r = response_temp.json()
                    if len(r["value"]) > 0:
                        value = float(r["value"][0]["value"])
                        name = r["station"]["name"]
                        if value > highest_temp:
                            highest_temp = value
                            highest_place = name
                        if value < lowest_temp:
                            lowest_temp = value
                            lowest_place = name
    return highest_place, highest_temp, lowest_place, lowest_temp

def main():
    parser = argparse.ArgumentParser(
        description="""Script to extract data from SMHI's Open API"""
    )
    parser.add_argument("--parameters", action="store_true", help="List SMHI API parameters")
    parser.add_argument("--temperatures", action="store_true", help="List highest/lowest temperatures")

    args = parser.parse_args()

    if args.parameters:
        smhi_parser = SmhiParser()
        response = smhi_parser.make_request()
        df = pd.DataFrame(columns=["key", "title", "summary"])
        if response.status_code == 200:
            for i, el in enumerate(response.json()["resource"]):
                df.loc[i] = [el["key"], el["title"], el["summary"]]
            df['key'] = df['key'].astype(int)
            df_sorted = df.sort_values(by='key', ascending=True)
            print(df_sorted.to_string(header=False, index=False))

    if args.temperatures:
        smhi_parser = SmhiParser()
        highest_place, highest_temp, lowest_place, lowest_temp = calculate_high_low_temperature(smhi_parser)
        print(f"Highest temperature: {highest_place}, {highest_temp} degrees")
        print(f"Lowest temperature: {lowest_place}, {lowest_temp} degrees")

if __name__ == "__main__":
    main()
