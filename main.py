import dataScraper
import threading
from time import time, sleep

games = []
threads = []
halftimes = [20, 5]
debug = True

def convert_string(temp):
    for i in range(len(temp) - 1):
        if temp[i] == ' ':
            temp = temp[0:i] + '+' + temp[i + 1:len(temp)]
    return temp

def gameRunning(myTeam, opTeam):
    game1 = dataScraper.game(myTeam, opTeam, threading.current_thread().ident)
    games.append(game1)
    half_pause = 0
    print("\nTime: " + game1.time)
    print(game1.myTeam + ": " + str(game1.myScore))
    print(game1.opTeam + ": " + str(game1.opScore))
    while(game1.updated[dataScraper.updateFlags.FULLTIME.value] != 1):
        if(game1.updated[dataScraper.updateFlags.OPTEAMSCORED.value]):
            print(game1.opTeam + " Scored :(")
        if(game1.updated[dataScraper.updateFlags.MYTEAMSCORED.value]):
            print(game1.myTeam + " Scored :)")

        #wait then update
        sleep(60 - time() % 60)
        if(game1.updated[dataScraper.updateFlags.HALFTIME.value]):
            print("Halftime")
            sleep(halftimes[half_pause]*60)
            half_pause = 1
        updated = game1.update()
        print("Time: " + game1.time)
        print(game1.myTeam + ": " + str(game1.myScore))
        print(game1.opTeam + ": " + str(game1.opScore))

    print("The game between " + game1.myTeam + " and " + game1.opTeam + " is over!")

    #Wait an hour bf removing the results of a finished game
    sleep(60 * 60)
    index = 0
    for game in games:
        index+=1
        if (game.tID == threading.current_thread().ident):
            games.remove(game)
            if (debug):
                print("Leaving game " + str(index))


def main():
    command = input("Is there more teams to add? (Y/N)")
    while(command == "Y"):
        myTeam = input("My Team:\n")
        opTeam = input("The Opposing Team:\n")
        myTeam = convert_string(myTeam)
        opTeam = convert_string(opTeam)
        t = threading.Thread(target=gameRunning, args=(myTeam, opTeam,))
        t.daemon = True
        t.start()
        threads.append(t)
        command = input("Is there more teams to add? (Y/N)")

    print("The program will run until the user cancels the program")
    command = input("Do you want to end the program? Y/N")
    while(command != "Y"):
        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        pass

main()