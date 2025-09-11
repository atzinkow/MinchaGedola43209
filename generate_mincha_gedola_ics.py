import os
import requests
from datetime import datetime, timedelta
from ics import Calendar, Event

LAT = 39.9681
LON = -82.9391
YEAR = datetime.now().year

def get_mincha_gedola(date):
    url = f"https://www.hebcal.com/zmanim?cfg=json&latitude={LAT}&longitude={LON}&date={date.strftime('%Y-%m-%d')}"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception(f"Failed to fetch data for {date.strftime('%Y-%m-%d')}: {resp.status_code}")
    data = resp.json()
    # Returns something like "2025-01-01T12:34:00-05:00"
    return data['times']['minchaGedola']

cal = Calendar()
start_date = datetime(YEAR, 1, 1)
end_date = datetime(YEAR, 12, 31)

curr = start_date
while curr <= end_date:
    print(f"Processing {curr.date()}")
    try:
        mg_time = get_mincha_gedola(curr)
        print(f"Fetched Mincha Gedola time: {mg_time}")
        dt = datetime.fromisoformat(mg_time)
        event = Event()
        event.name = "Mincha Gedola"
        event.begin = dt
        event.duration = timedelta(minutes=10)
        event.description = "Earliest time for Mincha today"
        cal.events.add(event)
        print(f"Added event for {curr.date()}")
    except Exception as e:
        print(f"Error on {curr.date()}: {e}")
    curr += timedelta(days=1)

os.makedirs('docs', exist_ok=True)
with open('docs/mincha_gedola.ics', 'w') as f:
    f.write(str(cal))
