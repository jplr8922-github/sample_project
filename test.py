import os
import json
import urllib.request
import ssl
import harvest
import pandas as pd
import base64
from dotenv import load_dotenv

class DataFetch:
    def __init__(self):
        """
        this is the __init__ of the object
        it fetch the variables in the .env file in order to connect to the Harvest account
        """
        ssl._create_default_https_context = ssl._create_unverified_context
        load_dotenv()
        self._account = os.getenv("HARVEST_ACCOUNT")
        self._email = os.getenv("HARVEST_EMAIL")
        self._password = os.getenv("HARVEST_PASSWORD")
        self._client = self.connect_to_harvest()

    def connect_to_harvest(self):
        """
        :return: this function return a harvest client
        """
        return harvest.Harvest(f"https://{self._account}.harvestapp.com", self._email, self._password)

    def query_harvest(self):
        """
        :return: this function connect to the harvest app, and fetch the data
        """
        url = f"https://{self._account}.harvestapp.com/daily"
        info = self._email + ":" + self._password
        encoded = base64.b64encode(bytes(info, "utf-8"))
        decoded = encoded.decode("utf-8")
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": "Basic (" + decoded + ")"
        }

        request = urllib.request.Request(url=url, headers=headers)
        response = urllib.request.urlopen(request, timeout=5)
        responseBody = response.read().decode("utf-8")
        jsonResponse = json.loads(responseBody)
        self.data = pd.DataFrame(jsonResponse["day_entries"])

    def show_data(self, nb=5):
        """
        :param nb: the number of line to display
        :return: will print the dataframe
        """
        print(self.data.head(nb))


