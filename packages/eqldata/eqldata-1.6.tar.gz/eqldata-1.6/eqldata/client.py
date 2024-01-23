import csv
import json
from io import StringIO

import requests
from websocket import create_connection
import time
from datetime import datetime

class DataClient:
    def __init__(self, auth_token, topics):
        self.uri = 'wss://api.equalsolution.net/ws1'
        self.headers = {"token": auth_token}
        self.topics = topics
        self.websocket = None
        self.is_listening = False

        self._start()

    def _start(self):
        self.connect()
        self.subscribe_to_topics(self.topics)

    def connect(self):
        self.websocket = create_connection(self.uri, header=self.headers)
        login_response = self.websocket.recv()
        try:
            login_data = json.loads(login_response)
            if login_data.get("status") == "Successfully Login!":
                print(login_response)
                return True
        except json.JSONDecodeError as e:
            print("JSON decode error:", e)
        return False

    def subscribe_to_topics(self, topics):
        if self.websocket is not None:
            subscribe_request = {
                "action": "subscribe",
                "topics": topics
            }
            self.websocket.send(json.dumps(subscribe_request))
        else:
            raise ValueError("WebSocket connection is not established.")

    def listen(self):
        while True:
            try:
                response = self.websocket.recv()
                if response is not None:
                    return response
            except Exception as e:
                print("Error:", e)
                self.reconnect()

    def reconnect(self):
        print("Connection lost. Reconnecting...")
        self.disconnect()
        time.sleep(5)  # Wait for a moment before reconnecting
        self.connect()

    def stop_listening(self):
        self.is_listening = False

    def disconnect(self):
        if self.websocket:
            self.websocket.close()

def generate_auth_token(username, password):
    try:
        auth_url = 'https://api.equalsolution.net/client/client_api_tocken'
        payload = {
            'email': username,
            'password': password
        }
        response = requests.post(auth_url, json=payload)
        if response.status_code == 200:
            return response.json().get('token')
        else:
            return response.json().get('detail')
    except requests.exceptions.RequestException as re:
        # Handle exceptions related to requests (network issues)
        print(f"RequestException: {re}")
        return None

    except Exception as e:
        # Catch any other unexpected exceptions
        print(f"Unexpected error: {e}")
        return None

def get_instrument_list(auth_token):
    try:
        instrument_url = 'https://api.equalsolution.net/client/get_instrument/'
        headers = {
            'Authorization': f'Bearer {auth_token}'
        }
        response = requests.post(instrument_url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return response.json().get('detail')
    except ValueError as ve:
        # Handle the case where there is an issue with the date format
        print(f"ValueError: {ve}")
        return None

    except requests.exceptions.RequestException as re:
        # Handle exceptions related to requests (network issues)
        print(f"RequestException: {re}")
        return None

    except Exception as e:
        # Catch any other unexpected exceptions
        print(f"Unexpected error: {e}")
        return None




def deserialize_binary_data(binary_data):
    decoded_content = binary_data.decode('utf-8')
    # Using StringIO to create a file-like object
    csv_file = StringIO(decoded_content)
    csv_reader = csv.reader(csv_file)
    data_dict = {}
    for row in csv_reader:
        instrument = row[0]
        # If the instrument is not in the dictionary, create a new entry
        if instrument not in data_dict:
            data_dict[instrument] = []
        # Append the row data to the corresponding instrument entry
        data_dict[instrument].append(row)
    # Convert the dictionary values to a list of lists
    data_list = list(data_dict.values())
    return data_list

def get_1MARKET_DATA(auth_token, instruments, for_date):
    try:
        xdate = datetime.strptime(for_date, "%Y-%m-%d").date()
        eod_url = 'https://api.equalsolution.net/client/download_daily_1'
        headers = {
            'Authorization': f'Bearer {auth_token}',
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        payload = {
            "instruments": instruments,
            "data_date": xdate.strftime("%Y-%m-%d")
        }
        response = requests.post(eod_url, headers=headers, json=payload)
        if response.status_code == 200:

            # Deserialize binary data into a structured format
            data_list = deserialize_binary_data(response.content)
            return data_list


        else:
            return response.json().get('detail')
    except ValueError as ve:
        # Handle the case where there is an issue with the date format
        print(f"ValueError: {ve}")
        return None

    except requests.exceptions.RequestException as re:
        # Handle exceptions related to requests (network issues)
        print(f"RequestException: {re}")
        return None

    except Exception as e:
        # Catch any other unexpected exceptions
        print(f"Unexpected error: {e}")
        return None


def get_EOD(auth_token, instruments, for_date):
    try:
        xdate = datetime.strptime(for_date, "%Y-%m-%d").date()
        eod_url = 'https://api.equalsolution.net/client/download_his_EOD'
        headers = {
            'Authorization': f'Bearer {auth_token}',
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        payload = {
            "instruments": instruments,
            "data_date": xdate.strftime("%Y-%m-%d")
        }
        response = requests.post(eod_url, headers=headers, json=payload)
        if response.status_code == 200:

            # Deserialize binary data into a structured format
            data_list = deserialize_binary_data(response.content)
            return data_list


        else:
            return response.json().get('detail')

    except ValueError as ve:
        # Handle the case where there is an issue with the date format
        print(f"ValueError: {ve}")
        return None

    except requests.exceptions.RequestException as re:
        # Handle exceptions related to requests (network issues)
        print(f"RequestException: {re}")
        return None

    except Exception as e:
        # Catch any other unexpected exceptions
        print(f"Unexpected error: {e}")
        return None

