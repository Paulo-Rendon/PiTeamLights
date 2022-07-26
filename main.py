import dataScraper
import threading
from time import time, sleep

halftimes = [20, 5]
def convert_string(temp):
    for i in range(len(temp) - 1):
        if temp[i] == ' ':
            temp = temp[0:i] + '+' + temp[i + 1:len(temp)]
    return temp

def gameRunning(myTeam, opTeam):
    half_pause = 0
    game1 = dataScraper.game(myTeam, opTeam)
    updated = [0, 0, 0, 0]
    print("\nTime: " + game1.time)
    print(game1.myTeam + ": " + str(game1.myScore))
    print(game1.opTeam + ": " + str(game1.opScore))
    if(game1.time == "Live" or game1.time == "Halftime"):
        while(not updated[dataScraper.updateFlags.FULLTIME.value]):
            if(updated[dataScraper.updateFlags.OPTEAMSCORED.value]):
                print(game1.opTeam + " Scored :(")
            if(updated[dataScraper.updateFlags.MYTEAMSCORED.value]):
                print(game1.myTeam + " Scored :)")

            #wait then update
            sleep(60 - time() % 60)
            if(updated[dataScraper.updateFlags.HALFTIME.value]):
                print("Halftime")
                sleep(halftimes[half_pause]*60)
                half_pause = 1
            updated = game1.update()
            print("Time: " + game1.time)
            print(game1.myTeam + ": " + str(game1.myScore))
            print(game1.opTeam + ": " + str(game1.opScore))

    print("The game between " + game1.myTeam + " and " + game1.opTeam + " is over!")

games = []
command = input("Is there more teams to add? (Y/N)")
while(command == "Y"):
    myTeam = input("My Team:\n")
    opTeam = input("The Opposing Team:\n")
    myTeam = convert_string(myTeam)
    opTeam = convert_string(opTeam)
    t = threading.Thread(target=gameRunning, args=(myTeam, opTeam,))
    t.start()
    games.append(t)
    command = input("Is there more teams to add? (Y/N)")

print("The program will run until the user cancels it or all games are ended")
for t in games:
    t.join()
    #for debugging purposes
    #myTeam = "Colombia"
    #opTeam = "Argentina"