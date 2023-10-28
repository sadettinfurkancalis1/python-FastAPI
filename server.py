"""
uvicorn server:app --reload

"""


import io
import pandas as pd
import requests
from fastapi import FastAPI, File, UploadFile, Form
from typing import List
import csv
import codecs
app = FastAPI()

BAUBUDDY_API_URL = "https://api.baubuddy.de/dev/index.php"
BAUBUDDY_API_LOGIN = {
    "username": "365",
    "password": "1"
}

COLOR_CODES_API_URL = "https://api.baubuddy.de/dev/index.php/v1/labels/{}"

def access_to_api():
    response = requests.post(
        "https://api.baubuddy.de/index.php/login",
        headers={
            "Authorization": "Basic QVBJX0V4cGxvcmVyOjEyMzQ1NmlzQUxhbWVQYXNz",
            "Content-Type": "application/json"
        },
        json=BAUBUDDY_API_LOGIN
    )
    response.raise_for_status()
    return response.json()["oauth"]["access_token"]

def create_labelid_endpoint(vehicle_list,access_header):
    for vehicle in vehicle_list:
        if vehicle["labelIds"] != None and vehicle["labelIds"] != "":
            color_code_endpoint = "https://api.baubuddy.de/dev/index.php/v1/labels/" + vehicle["labelIds"]
            color_code_response = requests.get(color_code_endpoint, headers=access_header)
            vehicle["labelIds"] = color_code_response.json()["colorCode"]
    return vehicle_list

def check_vehicles(csv_vehicles,old_vehicles):

    def fill_Nones(lst):
        for vehicle in lst:
            for key in vehicle.keys():
                if vehicle[key] is None:
                    vehicle[key] = ""
        return lst

    csv_vehicles = fill_Nones(csv_vehicles)
    old_vehicles = fill_Nones(old_vehicles)

    checked_data = []
    for csv_vehicle in csv_vehicles:
        for old_vehicle in old_vehicles:
            if csv_vehicle.items() <= old_vehicle.items():
                checked_data.append(old_vehicle)

    return checked_data

@app.post("/api/vehicles")
def submit_csv(file: UploadFile = File(...)):
    contents = file.file.read()
    buffer = io.StringIO(contents.decode('utf-8'))
    csvReader = list(csv.DictReader(buffer,delimiter = ';'))

    access_token = access_to_api()
    access_header = {"Authorization": f"Bearer {access_token}"}

    api_response = requests.get("https://api.baubuddy.de/dev/index.php/v1/vehicles/select/active",headers=access_header)
    vehicle_infos = api_response.json()

    checked_json = check_vehicles(csvReader,vehicle_infos)
    #last_json = [car for car in checked_json if car["hu"] != "" or None]

    return checked_json




