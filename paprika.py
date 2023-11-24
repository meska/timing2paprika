import json
from datetime import datetime
import os

import requests


class Paprika:
    clienti = []

    def __init__(self):
        self.session = requests.Session()
        if self.login(
                os.getenv("PAPRIKA_USERNAME"),
                os.getenv("PAPRIKA_PASSWORD"),
                os.getenv("PAPRIKA_PASSWORD2"),
                os.getenv("PAPRIKA_DB"),
        ):
            self.clienti = self.get_clienti()
            self.incarichi = self.get_incarichi()

    def login(self, username: str, password: str, password2: str, db: str) -> bool:
        print("Logging in Paprika")
        res = self.session.post(
            f'{os.getenv("PAPRIKA_URL")}/logOn/login',
            json={
                "USR_USERNAME": username,
                "USR_PASSWORD": password,
                "USR_PASSWORD2": password2,
                "DATABASE": db,
                "width": 2560,
                "height": 1440
            }

        )
        if res.status_code != 200:
            raise ValueError("Error logging in Paprika")
        if res.json().get('status') != True:
            raise ValueError(f"Error logging in Paprika: {res.json().get('message', '')}")
        return True

    def get_clienti(self) -> list:
        print("Getting clienti from Paprika")
        res = self.session.get(f'{os.getenv("PAPRIKA_URL")}/TBp0201/search/SA_SEARCH?search=&searchMc=false&limit=201')
        if res.status_code != 200:
            raise ValueError("Error getting clienti from Paprika")
        return res.json().get('result').get('SEARCH')

    def get_incarichi(self) -> int:
        print("Finding incarico in Paprika")
        res = self.session.post(
            f'{os.getenv("PAPRIKA_URL")}/wJTb0100/post/p1',
            headers={
                'Content-Type': 'text/plain'
            },
            data="""{
                "selectItems": [
                    {
                        "field": "JT_KEY",
                        "calculation": 0,
                        "width": 109,
                        "area": 1,
                        "unique": false,
                        "desc": "N° Incarico",
                        "flag": "",
                        "function": "",
                        "id": "",
                        "name": ""
                    },
                    {
                        "field": "JO_JOB_KEY",
                        "calculation": 0,
                        "width": 109,
                        "area": 1,
                        "unique": false,
                        "desc": "Nro. Progetto",
                        "flag": "",
                        "function": "",
                        "id": "",
                        "name": ""
                    },
                    {
                        "field": "JT_PE_STAFF_CODE_4",
                        "calculation": 0,
                        "width": 93,
                        "area": 1,
                        "unique": false,
                        "desc": "Assegnato a",
                        "flag": "",
                        "function": "",
                        "id": "",
                        "name": ""
                    },
                    {
                        "field": "JT_DATE_1",
                        "calculation": 0,
                        "width": 93,
                        "area": 1,
                        "unique": false,
                        "desc": "Data Inizio",
                        "flag": "",
                        "function": "",
                        "id": "",
                        "name": ""
                    },
                    {
                        "field": "JT_DATE_2",
                        "calculation": 0,
                        "width": 76,
                        "area": 1,
                        "unique": false,
                        "desc": "Data Fine",
                        "flag": "",
                        "function": "",
                        "id": "",
                        "name": ""
                    },
                    {
                        "field": "JT_SHORT_DESC",
                        "calculation": 0,
                        "width": 170,
                        "area": 1,
                        "unique": false,
                        "desc": "Descrizione",
                        "flag": "",
                        "function": "",
                        "id": "",
                        "name": ""
                    },
                    {
                        "field": "JT_DURATION",
                        "calculation": 0,
                        "width": 85,
                        "area": 1,
                        "unique": false,
                        "desc": "Durata",
                        "flag": "",
                        "function": "",
                        "id": "",
                        "name": ""
                    },
                    {
                        "field": "JT_ST_CODE",
                        "calculation": 0,
                        "width": 52,
                        "area": 1,
                        "unique": false,
                        "desc": "Status",
                        "flag": "",
                        "function": "",
                        "id": "",
                        "name": ""
                    }
                ],
                "whereItems": [
                    {
                        "field": "JT_PE_STAFF_CODE_4",
                        "operator": 31,
                        "canchange": true,
                        "or": false,
                        "name": "",
                        "value": "",
                        "value1": "",
                        "value2": "",
                        "tableItem": "JOB_TASK",
                        "id": ""
                    },
                    {
                        "field": "JT_ACTIVE",
                        "operator": 10,
                        "canchange": true,
                        "or": false,
                        "name": "",
                        "value": "",
                        "value1": "",
                        "value2": "",
                        "tableItem": "JOB_TASK",
                        "id": ""
                    },
                    {
                        "field": "ST_COMPLETE",
                        "operator": 11,
                        "canchange": true,
                        "or": false,
                        "name": "",
                        "value": "",
                        "value1": "",
                        "value2": "",
                        "tableItem": "STATUS",
                        "id": ""
                    }
                ],
                "whereTables": [],
                "optionItems": [
                    {
                        "item": "Options",
                        "values": [
                            "1",
                            "ST_COLOUR"
                        ]
                    }
                ],
                "sortItems": [
                    {
                        "field": "JT_KEY",
                        "direction": "ASC",
                        "subtotal": true,
                        "pageon": false,
                        "col": -1
                    }
                ],
                "subtotal": 0,
                "rows": [
                    {
                        "Name": "top",
                        "Height": 45
                    },
                    {
                        "Name": "body",
                        "Height": 17
                    },
                    {
                        "Name": "total",
                        "Height": 20
                    }
                ],
                "anal": {
                    "desc": null,
                    "widths": null,
                    "iso": null,
                    "selection": -1,
                    "field": null
                }
            }""".encode("utf-8")
        )
        if res.status_code != 200:
            raise ValueError("Error getting incarichi from Paprika")
        return res.json().get('result').get('records')

    def get_progetti_cliente(self, cliente_id):
        res = self.session.get(
            f'{os.getenv("PAPRIKA_URL")}/TBp0201/search/JO_SEARCH?search=&searchMc=false&samn={cliente_id}&date=20231124&limit=201')
        if res.status_code != 200:
            raise ValueError("Error getting progetti from Paprika")
        return res.json().get('result').get('JO_SEARCH')

    def add_entry(self, project: str, title: str, start_date: datetime, end_date: datetime) -> int:
        print("Adding entry to Paprika")

        # tacon temporaneo
        if project.lower() == 'pixartprinting':
            project = 'Pixart'

        cliente = list(filter(lambda x: x.get('SA_SHORTNAME').lower() == project.lower(), self.clienti))

        if len(cliente) == 0:
            listclienti = list(map(lambda x: x.get('SA_SHORTNAME').lower(), self.clienti))
            raise ValueError(f"Customer {project} not found in Paprika: {listclienti}")
        cliente = cliente[0]
        progetti = self.get_progetti_cliente(cliente.get('SA_MN'))

        # individuo l'incarico corretto in base ai progetti
        def filter_incarichi(x):
            job = x.get('JO_JOB_KEY')
            proj = list(filter(lambda x: x.get('JO_JOB_KEY') == job, progetti))
            if len(proj) == 0:
                return False
            # ignoro quelli scaduti
            job_end_date = datetime.fromisoformat(x.get('JT_DATE_2'))
            if datetime.now(tz=job_end_date.tzinfo) > job_end_date:
                return False
            return True

        incarichi_attivi = list(filter(filter_incarichi, self.incarichi))

        if len(incarichi_attivi) == 0:
            raise ValueError(f"No active incarichi found for customer {project}")

        incarico = incarichi_attivi[0]

        # trovato l'icarico, aggiungo l'entry
        # aggiungo timezone a start_date e a end_date
        job_id = incarico.get('JT_JO_MN')
        task_id = incarico.get('JT_MN')
        myself = 14  # TODO recuperare il mio id

        tot_time = round((end_date - start_date).total_seconds() / 3600, 2)

        payload = {
            "TB_MN": -1,
            "TB_JO_MN": job_id,
            "TB_JT_MN": task_id,
            "TB_PE_MN": myself,
            "TB_TOT_TIME": tot_time,
            "TB_ACTIVITY_TYPE": "DEVS",
            "TB_NARRATIVE": title,
            "TB_TIME_DATE": start_date.strftime("%Y-%m-%dT%H:%M:%S.000Z")
        }

        res = self.session.post(
            f'{os.getenv("PAPRIKA_URL")}/TimeModule/timemodulesave',
            json=payload,
        )
        if res.status_code != 200:
            raise ValueError("Error adding entry to Paprika")

        if res.json().get('status') != True:
            raise ValueError(f"Error adding entry to Paprika: {res.json().get('message', '')}")

        return res.json().get('result').get('TB').get('TB_MN') # TB_MN è il numero dell'entry salvata