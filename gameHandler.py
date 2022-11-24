# THIS IS FOR EDUCATIONAL PURPOSES ONLY, GOOGLE DOES NOT GIVE ME OR ANYONE PERMISSION
# FROM DATA SCRAPPING GOOGLE SEARCH RESULTS TO MAKE COMMERCIAL PROFIT

# This class is for the game handler, which will be in charge of
# updating the multiple games scores by calling the data scraper class
# as well as handle all of the threads that are assigned to each game

# Created by Paulo Rendon Jr: July 25th 2022
# Last updated by Paulo Rendon Jr: Oct. 5th 2022

import dataScraper
import threading
from time import time, sleep

class gameHandler:
    games = []
    threads = []
    halftimes = [20, 5]
    debug = False

    def __init__(self, debug):
        self.debug = debug
        if(debug):
            print("Game Handler built in debug mode")

    def convert_string(self, temp):
        for i in range(len(temp) - 1):
            if temp[i] == ' ':
                temp = temp[0:i] + '+' + temp[i + 1:len(temp)]
        return temp

    def gameRunning(self, myTeam, opTeam):
        game1 = dataScraper.game(myTeam, opTeam, threading.current_thread().ident, self.debug)
        self.games.append(game1)
        half_pause = 0
        if(self.debug):
            print("\nTime: " + game1.time)
            print(game1.myTeam + ": " + str(game1.myScore))
            print(game1.opTeam + ": " + str(game1.opScore))
        while(game1.updated[dataScraper.updateFlags.FULLTIME.value] != 1):
            if(game1.updated[dataScraper.updateFlags.OPTEAMSCORED.value] and self.debug):
                print(game1.opTeam + " Scored :(")
            if(game1.updated[dataScraper.updateFlags.MYTEAMSCORED.value] and self.debug):
                print(game1.myTeam + " Scored :)")

            #wait then update
            sleep(60 - time() % 60)
            if(game1.updated[dataScraper.updateFlags.HALFTIME.value]):
                if(self.debug):
                    print("Halftime")
                sleep(self.halftimes[half_pause]*60)
                half_pause = 1
            game1.update()
            if(self.debug):
                print("Time: " + game1.time)
                print(game1.myTeam + ": " + str(game1.myScore))
                print(game1.opTeam + ": " + str(game1.opScore))

        if(self.debug):
            print("The game between " + game1.myTeam + " and " + game1.opTeam + " is over!")

        #Wait an hour bf removing the results of a finished game
        sleep(60 * 60)

    def addingGame(self, myTeam, opTeam):
        #command = input("Is there more teams to add? (Y/N)")
        #while(command == "Y"):
        #myTeam = input("My Team:\n")
        #opTeam = input("The Opposing Team:\n")
        #myTeam = convert_string(myTeam)
        #opTeam = convert_string(opTeam)
        gameSize = len(self.games)
        t = threading.Thread(target=self.gameRunning, args=(myTeam, opTeam,))
        t.daemon = True
        t.start()
        self.threads.append(t)
        while(gameSize +1 != len(self.games)):
            continue
            #Wait till the thread adds the game to the "games" list
        gameSize+=1
        vals = [str(self.games[-1].myScore), str(self.games[-1].opScore), str(self.games[-1].time)]
        return vals

    def returnGames(self):
        return self.games