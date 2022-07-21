import requests
from bs4 import BeautifulSoup

def convert_string(temp):
    for i in range(len(temp) - 1):
        if temp[i] == ' ':
            temp = temp[0:i] + '+' + temp[i + 1:len(temp)]
    return temp

baseData = "https://google.com/search?q="

myTeam = input("My Team:\n")
opTeam = input("The Opposing Team:\n")

#for debugging purposes
myTeam = convert_string(myTeam)
opTeam = convert_string(opTeam)

myTeam = "Flamengo"
opTeam = "Juventude"
searchString = baseData + myTeam + "+vs+" + opTeam
response = requests.get(searchString)

print(searchString)
soup = BeautifulSoup(response.text, 'html.parser')
scores = soup.find_all("div", class_='BNeawe deIvCb AP7Wnd')
teams = soup.find_all("div", class_ = 'BNeawe s3v9rd AP7Wnd lRVwie')

time = teams[0].text
team1 = teams[1].text
team2 = teams[2].text
score1 = scores[1].text
score2 = scores[2].text

print("Time: " + time)
print(team1 + ": " + score1)
print(team2 + ": " + score2)
