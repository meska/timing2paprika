import os
from datetime import datetime

import requests


class Timing:
    def __init__(self):
        self.token = os.getenv("TIMING_TOKEN")
        self.url = os.getenv("TIMING_URL")

    def get_entries(self, from_date: datetime, to_date: datetime) -> list:
        d_format = "%Y-%m-%d %H:%M:%S"

        req = requests.get(
            f"{self.url}/time-entries?start_date_min={from_date.strftime(d_format)}&start_date_max={to_date.strftime(d_format)}&is_running=false&include_project_data=true&include_child_projects=true",
            headers={
                "Authorization": f"Bearer {self.token}"
            }
        )
        if req.status_code == 200:
            return req.json().get('data')

        raise ValueError(f"Error getting entries {req.reason}")

    def update_entry(self,entry:str, notes:str)-> bool:
        print(f"Update timing entry {entry} --> {notes}")
        res = requests.put(
            f"{self.url}{entry}",
            headers={
                "Authorization": f"Bearer {self.token}"
            },
            json={
                "notes":notes
            }
        )
        if res.status_code != 200:
            raise ValueError("Error Update Time Entry!")
