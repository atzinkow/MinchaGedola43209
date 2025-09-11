import requests
from datetime import datetime, timedelta
from ics import Calendar, Event

LAT = 39.9681
LON = -82.9391
YEAR = datetime.now().year

def get_mincha_gedola(date):
    url = f"https://www.myzmanim.com/day.aspx?cfg=json&lat={LAT}&lng={LON}&date={date.strftime('%Y-%m-%d')}"
    resp = requests.get(url)
    if resp.status_code != 200:
        raise Exception(f"Failed to fetch data for {date.strftime('%Y-%m-%d')}: {resp.status_code}")
    try:
        data = resp.json()
    except Exception as e:
        print(f"Response for {date.strftime('%Y-%m-%d')} was not valid JSON: {resp.text}")
        raise
    return data['times']['MinchaGedola']

cal = Calendar()
start_date = datetime(YEAR, 1, 1)
end_date = datetime(YEAR, 12, 31)

curr = start_date
while curr <= end_date:
    print(f"Processing {curr.date()}")
    try:
        mg_time = get_mincha_gedola(curr)
        dt = datetime.fromisoformat(mg_time)
        event = Event()
        event.name = "Mincha Gedola"
        event.begin = dt
        event.duration = timedelta(minutes=10)
        event.description = "Earliest time for Mincha today"
        cal.events.add(event)
    except Exception as e:
        print(f"Error on {curr.date()}: {e}")
    curr += timedelta(days=1)

import os
os.makedirs('docs', exist_ok=True)
with open('docs/mincha_gedola.ics', 'w') as f:
    f.writelines(cal)
