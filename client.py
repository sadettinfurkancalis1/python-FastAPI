import pandas as pd
import requests
import argparse
import pandas
from datetime import datetime


server_url = "http://localhost:8000/api/vehicles"

file_path = "vehicles.csv"
file_name = "vehicles.csv"
def post_csv_to_server(csv_path,keys,colored=True):
    print()


if __name__ == "__main__":

    with open(file_path, "rb") as file:
        files = {"file": (file_name, file, "multipart/form-data")}
        response = requests.post(server_url, files=files)

    if response.status_code == 200:
        api_response = response.json()
        print(api_response)

        parser = argparse.ArgumentParser(description="Client Script")
        parser.add_argument("-k", "--keys", help="list of keys")
        parser.add_argument("-c", "--colored", default=True, help="Flag to enable coloring")
        parser.add_argument("-f", "--file", default="vehicles.csv")

        args = parser.parse_args()
        #post_csv_to_server()
    else:
        print(f"request is failed status code = {response.status_code}: {response.text}")


