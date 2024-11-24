import requests
import csv
from datetime import date

userID = 1123120136
csvFile = "log.csv"

def getUserFriendsID():
    URL = f"https://friends.roblox.com/v1/users/{userID}/friends"

    friendList = requests.get(url=URL).json()["data"]
    FriendsID = [i["id"] for i in friendList]

    return FriendsID

def CSVEmpty():
    FriendsID = getUserFriendsID()

    with open(csvFile, "a", newline='') as File:
        csvWriter = csv.writer(File, delimiter=";")
        csvWriter.writerow(["lastTimeChecked", "Changes", "Date (YYYY-MM-DD)"])
        csvWriter.writerow([FriendsID, [], date.today()])

def CSVUpdate():
    lastTimeChecked = []
    Changes = []

    try:
       with open(csvFile, "r") as File:
            csvReader = csv.reader(File, delimiter=";")
            rows = list(csvReader)
            if rows:
                lastRowOld = rows[-1][0]
                lastTimeChecked = list(map(int, lastRowOld.strip('[]').split(', ')))
    except FileNotFoundError:
        CSVEmpty()
        return "CSV file not found, creating a new file."

    FriendsID = getUserFriendsID()

    FriendsID_set = set(FriendsID)
    lastTimeChecked_set = set(lastTimeChecked)
    
    unfriended = lastTimeChecked_set - FriendsID_set
    Changes.extend([[list(unfriended), "unfriended"]])
    
    new_friends = FriendsID_set - lastTimeChecked_set
    Changes.extend([[list(new_friends), "newFriends"]])

    with open(csvFile, "a", newline='') as File:
        csvWriter = csv.writer(File, delimiter=";")
        csvWriter.writerow([FriendsID, Changes, date.today()])
    
    return Changes

print(CSVUpdate())
