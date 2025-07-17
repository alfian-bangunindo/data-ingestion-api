import os
import sys
import requests
import pysftp
import json
from datetime import datetime
import csv
from dotenv import load_dotenv


load_dotenv()

SFTP_HOST = os.environ["SFTP_HOST"]
SFTP_USER = os.environ["SFTP_USER"]
SFTP_PASSWORD = os.environ["SFTP_PASSWORD"]
SFTP_PORT = int(os.environ["SFTP_PORT"])

API_URL = "https://api.ekraf.go.id/posts"
DATA_DIR = "data"

CURRENT_DATE = datetime.now().strftime("%Y_%m_%d")

if not os.path.exists(DATA_DIR):
    print("Data directory is not exists")
    print("Initailizing data directory...")
    os.makedirs(DATA_DIR)
    print("===================================")

def extract() -> str | None:
    print("Attempting to call Ekraf API...")
    try:
        response = requests.get(API_URL)
        raw_data = response.json()
        print("API call successful!")

        raw_data_path = f"{DATA_DIR}/raw_data_{CURRENT_DATE}.json"

        with open(raw_data_path, "w") as fp:
            json.dump(raw_data, fp)
        
        print(f"Raw data saved in local path: {raw_data_path}")

        return raw_data_path

    except Exception as e:
        print(f"Something went wrong: {e}")

def transform(data_extraction_path: str) -> str | None:
    with open(data_extraction_path, "r") as fp:
        data = json.load(fp)["data"]
    
    print("Transforming data...")
    for d in data:
        d.pop("content")
        d.pop("content_html")

        d["user_name"] = d["user"]["name"]
        d["user_email"] = d["user"]["id"]
        d.pop("user")
        
        categories = []
        for c in d["categories"]:
            categories.append(c["title"])
        
        categories = "|".join(categories)
        d["categories"] = categories

        tags = []
        for t in d["tags"]:
            tags.append(t["name"])
        tags = "|".join(tags)
        d["tags"] = tags

    headers = data[0].keys()
    print("Data transform successful!")    

    transformed_data_path = f"{DATA_DIR}/transformed_data_{CURRENT_DATE}.json"
    
    try:
        with open(transformed_data_path, "w", newline="") as fp:
            writer = csv.DictWriter(fp, fieldnames=headers)
            
            writer.writeheader()
            writer.writerows(data)
        
        print(f"Transformed data saved in local path: {transformed_data_path}")
        return transformed_data_path
    
    except Exception as e:
        print(f"Fail to write transformed data: {e}")

def load(data_transformation_path: str):
    print(f"Attempting to create a connection to SFTP Server...")
    try:
        cnopts = pysftp.CnOpts()
        with pysftp.Connection(
            host=SFTP_HOST,
            username=SFTP_USER,
            port=SFTP_PORT,
            password=SFTP_PASSWORD,
            cnopts=cnopts
        ) as sftp:
            print(f"Connection created successfully!")
            remote_path = f"/uploads/transformed_data_{CURRENT_DATE}.csv"
            sftp.put(data_transformation_path, remote_path)  
            print(f"Data loaded from local path: {data_transformation_path} to remote path: {remote_path}")

    except Exception as e:
        print(f"Something went wrong: {e}")

if __name__ == "__main__":
    data_extraction_path = extract()
    if not data_extraction_path:
        print("Data extraction is failed!")
        sys.exit()
    
    print("===================================")

    data_transformation_path = transform(data_extraction_path)
    if not data_transformation_path:
        print("Data transformation is failed!")
        sys.exit()

    print("===================================")

    load(data_transformation_path)


