import requests
import argparse
import pandas
from datetime import datetime

SERVER_API_URL = "http://localhost:8000/submit_csv/"




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Client Script")
    parser.add_argument("-k","--keys",help="list of keys")
    parser.add_argument("-c","--colored",default=True,help="Flag to enable coloring")
    parser.add_argument("-f","--file",default="vehicles.csv")

    args = parser.parse_args()
