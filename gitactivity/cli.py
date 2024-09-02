import requests
import json
import sys
import pyinputplus as pyip
import datetime
import re



def oneMonthDiff(item):
    date_pattern = r'\b(\d{4})-(\d{2})-(\d{2})T\d{2}:\d{2}:\d{2}Z\b'
    today = datetime.datetime.today()

    dt = item["created_at"]
    match = re.search(date_pattern, dt)
    if match:
        dtyear = match.group(1)
        dtmonth = match.group(2)
        dtday = match.group(3)

    dt2 = datetime.datetime(int(dtyear),int(dtmonth),int(dtday))

    diffrence = today - dt2
    

    if diffrence.days <= 30:
        return True
    else:
        return False


def recentActivity(name):
   
    url = f"https://api.github.com/users/{name}/events"
    response = requests.get(url).json()

    try:
        for item in response:
            if oneMonthDiff(item):
                for key, value in item.items():
                    if key == "type":
                        match value:
                            case "IssuesEvent":
                                print(f"{item["payload"]["action"]} issue")
                            case "PushEvent":
                                print(f"Pushed {len(item["payload"]["commits"])} commits to {item["repo"]["name"]}")
                            case "CreateEvent":
                                print(f"Created new {item["payload"]["ref_type"]}")
                            case "WatchEvent":
                                print(f"Starred {item["repo"]["name"]}")
                            case "ForkEvent":
                                print(f"Forked {item["payload"]["forkee"]["name"]} repository")
    except KeyError:
        print("This users recent activity is private or does not exist.")
if __name__ == '__main__':

    username = pyip.inputStr("Enter git username: ", blockRegexes=[r"\s"])

    print("All activity in the last month: \n")
    recentActivity(username)

