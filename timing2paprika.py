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
