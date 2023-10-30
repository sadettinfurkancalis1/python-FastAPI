"""
to run this server use =
uvicorn server:app --reload

"""

import io
import requests
import yaml
from fastapi import FastAPI, File, UploadFile
import csv

app = FastAPI()

with open("config.yml","r") as file:
    init_settings = yaml.safe_load(file)


def access_to_api():
    """
    accessing api for Authorization token
    :return:
    """
    response = requests.post(
        url= init_settings["baubuddy"]["login_url"],
        headers=init_settings["baubuddy"]["headers"],
        json=init_settings["baubuddy"]["login"]
    )
    return response.json()["oauth"]["access_token"]


def create_labelid_endpoint(vehicle_list, access_header):
    """
    Get colorCodes from API if exist in
    vehicle's labelId endpoint
    """
    for vehicle in vehicle_list:
        if vehicle["labelIds"] is not None and vehicle["labelIds"] != "":
            color_code_endpoint = init_settings["baubuddy"]["labels_url"] + vehicle["labelIds"]
            color_code_response = requests.get(color_code_endpoint, headers=access_header)
            vehicle_list["colorCode"] = color_code_response.json()["colorCode"]
    return vehicle_list


def check_vehicles(csv_vehicles, api_vehicles):
    """
    Checking api datas and vehicle datas
    and returning one merged data
    """

    def fill_nones(lst):
        """
        filling none with "" because when comparing
        with another data it becomes problem
        """
        for vehicle in lst:
            for key in vehicle.keys():
                if vehicle[key] is None:
                    vehicle[key] = ""
        return lst

    def add_checked_data(data, vehicle_list):
        """
        checking if data["hu"] is empty or not
        and returning with nonempty datas
        """
        for vehicle in vehicle_list:
            if "hu" in vehicle and vehicle["hu"] != "":
                data.append(vehicle)
        return data

    csv_vehicles = fill_nones(csv_vehicles)
    api_vehicles = fill_nones(api_vehicles)

    checked_data = add_checked_data([], csv_vehicles)
    checked_data = add_checked_data(checked_data, api_vehicles)

    return checked_data

@app.post("/api/vehicles")
def submit_csv(file: UploadFile = File(...)):
    # Csv reading Part
    contents = file.file.read()
    buffer = io.StringIO(contents.decode('utf-8'))
    csv_reader = list(csv.DictReader(buffer, delimiter=';'))

    # find access token and send request to API
    access_token = access_to_api()
    access_header = {"Authorization": f"Bearer {access_token}"}
    api_response = requests.get(
        init_settings["baubuddy"]["vehicles_url"],
        headers=access_header
    )

    # vehicle_infos = create_labelid_endpoint(vehicle_infos,access_header) # try to find solution
    vehicle_infos = api_response.json()
    checked_json = check_vehicles(csv_reader, vehicle_infos)

    return checked_json
