#!/usr/bin/env python

from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import requests
import json
import os

def clean_id(data):
    if isinstance(data, dict):
        for key, value in data.items():
            if key == 'id':
                data[key] = list(set(data[key]))
            else:
                clean_id(value)
    elif isinstance(data, list):
        for item in data:
            clean_id(item)

codexData = requests.get("https://lostarkcodex.com/us/eventcalendar/", headers={"User-Agent": UserAgent().getChrome['useragent']})

rawsoup = BeautifulSoup(codexData.content, features="html.parser")
coldsoup = rawsoup.find_all(lambda tag: tag.name=="script" and "calendar" in tag.text)

for s in coldsoup:
    if (str(s).find("calendar_data") < 0 and str(s).find("calendar_events") < 0):
        print("Could not find any calendar data or events")
        exit(1)

soup=(str(coldsoup[0])).splitlines()
calendar_data=soup[1]
idx = calendar_data.find("{")
idy = calendar_data.rfind(";")  if calendar_data.rfind(";") >= 0 else ""
calendar_data = json.loads(f"""{calendar_data[idx:idy] if idy else calendar_data[idx:]}""")

clean_id(calendar_data)

os.replace("data/data.json","data/data.old.json")
with open("data/data.json", "w+") as soupfile:
    json.dump(calendar_data, soupfile, sort_keys=True)
    
calendar_events=soup[2]
idx = calendar_events.find("{")
idy = calendar_events.rfind(";")  if calendar_events.rfind(";") >= 0 else ""
calendar_events = json.loads(f"""{calendar_events[idx:idy] if idy else calendar_events[idx:]}""")

with open ("data/events.json", "r+", encoding="utf-8") as evdata:
    evjson = json.load(evdata)
with open ("public/locales/en/events.json", "r+", encoding="utf-8") as evlocaledata:
    evlocalejson = json.load(evlocaledata)

addedEvents = []
for ev in calendar_events:
    if ev not in evjson:
        addedEvents.append(ev)
        evjson[ev] = calendar_events[ev]
        evlocalejson[ev] = calendar_events[ev][0]

if (len(addedEvents) > 0):
    print(f"Added {addedEvents} to the events json")
with open ("data/events.json", "w", encoding="utf-8") as evdata:
    json.dump(evjson,evdata,sort_keys=True)
with open ("public/locales/en/events.json", "w", encoding="utf-8") as evlocaledata:    
    json.dump(evlocalejson,evlocaledata,sort_keys=True)

print("Events successfully updated")
