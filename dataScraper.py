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
    myTeam = opTeam = searchString = time = ""
    myScore = opScore = 0

    def __init__(self, team1, team2):
        self.myTeam = team1
        self.opTeam = team2
        self.searchString = baseData + team1 + "+vs+" + team2
        self.update()

    def update(self):
        updated = [0, 0, 0, 0]
        response = requests.get(self.searchString)

        #print(searchString)
        soup = BeautifulSoup(response.text, 'html.parser')
        scores = soup.find_all("div", class_='BNeawe deIvCb AP7Wnd')
        teams = soup.find_all("div", class_='BNeawe s3v9rd AP7Wnd lRVwie')

        #haven't checked the actual halftime syntax yet
        if (teams[0].text == "Halftime"):
            updated[updateFlags.HALFTIME.value] = 1
        elif (teams[0].text != "Live"):
            updated[updateFlags.FULLTIME.value] = 1
        self.time = teams[0].text
        if(self.myTeam == teams[1].text):
            if(self.myScore < int(scores[1].text)):
                updated[updateFlags.MYTEAMSCORED.value] = 1
            self.myScore = int(scores[1].text)
            if(self.opScore < int(scores[2].text)):
                updated[updateFlags.OPTEAMSCORED.value] = 1
            self.opScore = int(scores[2].text)

        else:
            if (self.myScore < int(scores[1].text)):
                updated[updateFlags.MYTEAMSCORED.value] = 1
            self.myScore = int(scores[2].text)
            if (self.opScore < int(scores[2].text)):
                updated[updateFlags.OPTEAMSCORED.value] = 1
            self.opScore = int(scores[1].text)

            return updated


