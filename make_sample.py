import glob
import zipfile

import pandas as pd

COLS = ["Year", "Quarter", "Month", "DayofMonth", "DayOfWeek", "FlightDate",
        "Reporting_Airline", "Tail_Number", "Flight_Number_Reporting_Airline",
        "Origin", "OriginState", "Dest", "DestState",
        "CRSDepTime", "DepTime", "DepDelay", "DepDel15", "DepTimeBlk", "TaxiOut",
        "CRSArrTime", "ArrDelay", "ArrDel15", "Cancelled", "CancellationCode", "Diverted",
        "CRSElapsedTime", "Flights", "Distance", "DistanceGroup",
        "CarrierDelay", "WeatherDelay", "NASDelay", "SecurityDelay", "LateAircraftDelay"]
FRAC = 0.1


def read(path):
    with zipfile.ZipFile(path) as z:
        name = [n for n in z.namelist() if n.endswith(".csv")][0]
        return pd.read_csv(z.open(name), usecols=COLS)[COLS]


df = pd.concat([read(f) for f in sorted(glob.glob("us-flights-2026-raw/monthly-zips/*.zip"))],
               ignore_index=True)
speed = df.Distance / (df.CRSElapsedTime / 60)
defects = df.CRSElapsedTime.isna() | (df.CRSElapsedTime <= 0) | (speed > 600)
sample = pd.concat([df.sample(frac=FRAC, random_state=0), df[defects]])
sample = sample[~sample.index.duplicated()].sort_index()
sample.to_csv("flights_2026_sample.zip", index=False,
              compression={"method": "zip", "archive_name": "flights_2026_sample.csv"})
print(len(df), "->", sample.shape, "| строк с дефектами:", int(defects.sum()))
