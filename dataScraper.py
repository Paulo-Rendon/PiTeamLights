# THIS IS FOR EDUCATIONAL PURPOSES ONLY, GOOGLE DOES NOT GIVE ME OR ANYONE PERMISSION
# FROM DATA SCRAPPING GOOGLE SEARCH RESULTS TO MAKE COMMERCIAL PROFIT

# This class is in charge of data scraping from Google to update
# game scores

# Created by Paulo Rendon Jr: July 20th 2022
# Last updated by Paulo Rendon Jr: Oct. 5th 2022


import requests
from bs4 import BeautifulSoup
from enum import Enum

baseData = "https://google.com/search?q="

class updateFlags(Enum):
    MYTEAMSCORED = 0
    OPTEAMSCORED = 1
    HALFTIME = 2
    FULLTIME = 3

class game:
    myTeam = opTeam = searchString = time = tID = ""
    myScore = opScore = 0
    updated = [0, 0, 0, 0]
    debug = False

    def __init__(self, team1, team2, threadID, debug):
        self.myTeam = team1
        self.opTeam = team2
        self.tID = threadID
        self.searchString = baseData + team1 + "+vs+" + team2
        self.debug = debug
        if self.debug:
            print("Creating Data Scraper in debug mode for " + self.myTeam +" vs " + self.opTeam)
        self.update()

    def update(self):
        self.updated = [0, 0, 0, 0]
        response = requests.get(self.searchString)

        #print(searchString)
        soup = BeautifulSoup(response.text, 'html.parser')
        scores = soup.find_all("div", class_='BNeawe deIvCb AP7Wnd')
        teams = soup.find_all("div", class_='BNeawe s3v9rd AP7Wnd lRVwie')
        check = soup.find_all("span", class_='rQMQod AWuZUe')
        if(self.debug):
            print("Scores: ")
            print(scores)
            print("\nTeams: ")
            print(teams)
            f = open("page.html", "w")
            f.write(response.text)
            f.close()
        #haven't checked the actual halftime syntax yet
        if (teams[0].text == "Halftime"):
            self.updated[updateFlags.HALFTIME.value] = 1
        elif (len(check) == 0 or check[0].text != teams[0].text):
            self.updated[updateFlags.FULLTIME.value] = 1
        self.time = teams[0].text
        if(self.myTeam == teams[1].text):
            if(self.myScore < int(scores[1].text)):
                self.updated[updateFlags.MYTEAMSCORED.value] = 1
            self.myScore = int(scores[1].text)
            if(self.opScore < int(scores[2].text)):
                self.updated[updateFlags.OPTEAMSCORED.value] = 1
            self.opScore = int(scores[2].text)

        elif(self.myTeam == teams[2].text):
            if (self.myScore < int(scores[2].text)):
                self.updated[updateFlags.MYTEAMSCORED.value] = 1
            self.myScore = int(scores[2].text)
            if (self.opScore < int(scores[1].text)):
                self.updated[updateFlags.OPTEAMSCORED.value] = 1
            self.opScore = int(scores[1].text)

        else:
            print("Game Not Found!")
            self.updated[updateFlags.FULLTIME.value] = 1


