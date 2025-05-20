import os
import requests
from pathlib import Path


class BunnyCDNStorage:
    def __init__(self, BUNNY_CDN_STORAGE_APIKEY, BUNNY_CDN_STORAGE_ZONE, BUNNY_CDN_PULL_ZONE):
        self.apikey       = BUNNY_CDN_STORAGE_APIKEY
        self.storage_zone = BUNNY_CDN_STORAGE_ZONE
        self.pull_zone    = BUNNY_CDN_PULL_ZONE

        self.base_url     = f'https://storage.bunnycdn.com/{ self.storage_zone }/'
        self.headers      = {
            'AccessKey'    : self.apikey,
            'Content-Type' : 'application/json',
            'Accept'       : 'applcation/json'
        }

    def download_file(self, file_path, destination_path):
        file_url      = f'{ self.base_url }{ file_path }'
        file_name     = file_url.split("/")[-1]
        download_path = Path(destination_path, file_name)

        print(f"Attempting to download from: {file_url}")
        print(f"Will save to: {download_path}")

        try:
            headers = {
                'AccessKey': self.apikey,
                'accept': '*/*'
            }

            print(f"Using headers: {headers}")

            # Set a timeout to avoid hanging indefinitely
            response = requests.get(file_url, headers=headers, stream=True, timeout=10)

            # Print response status and headers for debugging
            print(f"Response status: {response.status_code}")
            print(f"Response headers: {response.headers}")

            if response.status_code != 200:
                print(f"Error response content: {response.text}")
                return response.status_code

            response.raise_for_status()

            # Create destination directory if it doesn't exist
            if os.path.dirname(str(download_path)):
                os.makedirs(os.path.dirname(str(download_path)), exist_ok=True)

            with open(download_path, "wb") as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)

            print(f"File downloaded successfully to {download_path}")
            return response.status_code
        except requests.exceptions.Timeout:
            print("Request timed out. The server may be unavailable or the file may be too large.")
            return "Timeout Error"
        except requests.exceptions.HTTPError as http_err:
            print(f"HTTP Error: {http_err}")
            return http_err
        except Exception as error:
            print(f"Error downloading file: {error}")
            return error

    def upload_file(self, storage_path, file_path, file_name=None):
        try:
            if file_name is None:
                file_name = Path(file_path).name

            storage_url = f'{self.base_url}{storage_path}{file_name}'

            headers = {
                'AccessKey': self.apikey,
                'Content-Type': 'application/octet-stream',
                'Accept': 'application/json'
            }

            with open(file_path, 'rb') as file_data:
                response = requests.put(storage_url, headers=headers, data=file_data)

            response.raise_for_status()
            cdn_url = f'https://{self.pull_zone}.b-cdn.net/{storage_path}{file_name}'
            return cdn_url
        except Exception as error:
            return error

    def object_exists(self, file_path):
        file_url = f'{ self.base_url }{ file_path }'
        response = requests.get(file_url, headers=self.headers)
        return response.status_code == 200

    def delete_object(self, file_path):
        try:
            file_url = f'{ self.base_url }{ file_path }'
            response = requests.delete(file_url, headers=self.headers)
            response.raise_for_status()
            return response.status_code
        except Exception as error:
            return error
