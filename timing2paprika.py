"""
Sync Timing App to Infinity
"""

from datetime import datetime, timedelta

from paprika import Paprika
from timing import Timing


class Timing2Paprika:
    def __init__(self):
        self.timing = Timing()
        self.paprika = None

    def run(self, from_date: datetime = None, to_date: datetime = None, customer=None):
        if from_date is None:
            from_date = datetime.now() - timedelta(days=2)
        if to_date is None:
            to_date = datetime.now() + timedelta(days=1)

        # entries = json.loads(
        #    '[{"self": "/time-entries/3652492960070895360", "start_date": "2023-11-23T08:05:29.034261+00:00", "end_date": "2023-11-23T11:20:48.808793+00:00", "duration": 11719.774532, "project": {"self": "/projects/3520914886232515072", "team_id": null, "title": "PixartPrinting", "title_chain": ["Quamm", "PixartPrinting"], "color": "#30779EFF", "productivity_score": 1, "is_archived": false, "parent": {"self": "/projects/3513417058817328735"}}, "title": "Gql Proxy", "notes": null, "is_running": false, "creator_name": "meskatech@gmail.com"}]')

        entries = self.timing.get_entries(from_date, to_date)

        # filter entries that have 'PAPRIKA_ID' in notes ( already synced )
        def exclude_done(x):
            if x.get("notes") is None:
                return True
            return x.get("notes").find("PAPRIKA_ID") == -1

        entries = list(filter(exclude_done, entries))

        if customer:
            # filter entries by customer ( parent node )
            def filter_customer(x):
                if x.get("project") is None:
                    return False
                return x.get("project").get("title_chain", [""])[0] == customer

            entries = list(filter(filter_customer, entries))

        if entries:
            self.paprika = Paprika()

            for entry in entries:
                start_date = datetime.strptime(
                    entry.get("start_date"), "%Y-%m-%dT%H:%M:%S.%f%z"
                )
                end_date = datetime.strptime(
                    entry.get("end_date"), "%Y-%m-%dT%H:%M:%S.%f%z"
                )

                paprika_id = self.paprika.add_entry(
                    project=entry.get("project").get("title"),
                    title=entry.get("title"),
                    start_date=start_date,
                    end_date=end_date,
                )

                self.timing.update_entry(
                    entry.get("self"), notes=f"PAPRIKA_ID:{paprika_id}"
                )
        else:
            print("No entries to sync")
