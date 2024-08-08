import os
from datetime import datetime, timedelta
from time import sleep

import sentry_sdk
from dotenv import load_dotenv

from timing2paprika import Timing2Paprika

sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    traces_sample_rate=0.2,
)

load_dotenv()

if __name__ == "__main__":
    print("Starting Timing2Paprika")
    t2p = Timing2Paprika(telegram=True)

    # loop ogni ora
    while True:
        from_date = datetime.now() - timedelta(days=7)
        t2p.run(from_date=from_date, customer="Quamm")
        print("Sleeping for 1 hour")
        print("--------------------------------")
        sleep(3600)
