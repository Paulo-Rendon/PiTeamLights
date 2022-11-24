# THIS IS FOR EDUCATIONAL PURPOSES ONLY, GOOGLE DOES NOT GIVE ME OR ANYONE PERMISSION
# FROM DATA SCRAPPING GOOGLE SEARCH RESULTS TO MAKE COMMERCIAL PROFIT

# I am going to use Kivy to do the display bc it offers beautiful design
# and seems very capable when it comes to working on the raspberry Pi and even
# gives me the option to export to android in the future if I wish (prob pay for API access
# before I decide to export to android)

# Created by Paulo Rendon Jr: Sep. 19th 2022
# Last updated by Paulo Rendon Jr: Oct. 5th 2022

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.lang import Builder
import gameHandler
import threading
from kivy.uix.image import Image
from dataScraper import updateFlags
from functools import partial

debug = True
Builder.load_string('''
<GreyGrid>
    canvas.before:
        Color:
            rgba: 0.5, 0.5, 0.5, 1
        RoundedRectangle:
            size: self.size
            pos: self.pos
            radius: [(40, 40), (40, 40), (40, 40), (40, 40)]
''')

class GreyGrid(GridLayout):
    pass
#The main class obj created for display
class appDisplay(App):

    # This function is the default screen constructor
    def build(self):

        # Builds the gamehandler obj
        self.gamehandler = gameHandler.gameHandler(debug)
        # For holding all gamecontainers
        self.gameContainers = []
        self.window = BoxLayout()
        self.window.orientation = "vertical"
        self.grid = GridLayout()
        self.grid.cols = 2
        self.grid.spacing = 5
        self.grid.padding = 10
        #side margin 60%, top bottom margin 70%
        self.grid.size_hint = (0.6, 0.7)
        self.grid.pos_hint = {"center_x":0.5, "center_y":0.5}

        #add widgets to window
        self.button = Button(
                        text="Add Game",
                        size_hint=(0.1, 0.1),
                        pos_hint={"center_x": 0.9, "y":1},
                        bold=True,
                        background_color = "#00FFCE",
                        #This makes the button color more close to color specified
                        background_normal=""
                        )
        self.button.bind(on_press=self.addGameBtn)
        self.window.add_widget(self.button)
        self.window.add_widget(self.grid)

        #Schedule updateScreen to run every minute
        #The lambda is to specify that updateScreen takes no arguments and the 1 provided is for the Clock obj
        Clock.schedule_interval(lambda dt: self.updateScreen(), 60)


        return self.window

    # This is the popup object for when the add game button is pressed
    def addGameBtn(self, instance):
        addGameLayout = GridLayout()
        addGameLayout.cols = 2
        yourTeamText = Label(text='Your Team:',
                             font_size=14,
                             size_hint=(0.5, 0.1))
        opTeamText = Label(text='Opposing Team',
                           font_size=14,
                           size_hint=(0.5, 0.1))
        self.yourTeam = TextInput(
                    multiline=False,
                    padding_y = (20,20),
                    size_hint=(0.5, 0.1)
                    )
        self.opTeam = TextInput(
                    multiline=False,
                    padding_y = (20,20),
                    size_hint=(0.5, 0.1)
        )
        subButton = Button(
                        text="submit",
                        size_hint=(0.1, 0.1),
                        #pos_hint={"center_x": 0.9, "y":1},
                        bold=True,
                        background_color = "#00FFCE",
                        #This makes the button color more close to color specified
                        background_normal=""
                        )
        subButton.bind(on_press = self.addGameToScreen)
        exitButton = Button(
                        text="close",
                        size_hint=(0.1, 0.1),
                        #pos_hint={"center_x": 0.9, "y":1},
                        bold=True,
                        background_color = "#00FFCE",
                        #This makes the button color more close to color specified
                        background_normal=""
                        )
        exitButton.bind(on_press = lambda arg : self.addGame.dismiss())

        # add defined objects to layout
        addGameLayout.add_widget(yourTeamText)
        addGameLayout.add_widget(opTeamText)
        addGameLayout.add_widget(self.yourTeam)
        addGameLayout.add_widget(self.opTeam)
        addGameLayout.add_widget(subButton)
        addGameLayout.add_widget(exitButton)

        #self.greeting.text = "Hello " + self.user.text + "!"
        self.addGame = Popup(title='Add Game',
                      content=addGameLayout,
                      size_hint=(None, None), size=(400, 400))
        self.addGame.open()


    # This function adds the game container to the screen
    # Should be called by the main thread since it includes GUI altering
    def addGameToScreen(self, instance):
        if(debug):
            print("Adding game between " + self.yourTeam.text + " and " + self.opTeam.text)

        # Add game to game handler
        vals = self.gamehandler.addingGame(self.yourTeam.text, self.opTeam.text)
        self.addGame.dismiss()  #close popup

        # Change grid layout to fit more reasonably when displayed
        self.grid.cols = len(self.gamehandler.games) // 2
        if (len(self.gamehandler.games) % 2):
            self.grid.cols += 1

        # Build a game Container (setup for dubugging using hard values)
        gameContainer = GreyGrid()
        gameContainer.rows = 2

        yourTeamText = Label(text=str(self.yourTeam.text),
                             font_size=14,
                             size_hint=(0.5, 0.1))
        opTeamText = Label(text=str(self.opTeam.text),
                           font_size=14,
                           size_hint=(0.5, 0.1))
        gameContainer.yourTeamScore = Label(text=str(vals[0]),
                              font_size=14,
                              size_hint=(0.5, 0.1))
        gameContainer.opTeamScore = Label(text=str(vals[1]),
                            font_size=14,
                            size_hint=(0.5, 0.1))
        gameContainer.time = Label(text=str(vals[2]),
                     font_size=14,
                     size_hint=(0.5, 0.1))

        dash = Label(text="-",
                     font_size=21,
                     size_hint=(0.5, 0.1))

        # Add objects to layout
        gameContainer.add_widget(yourTeamText)
        gameContainer.add_widget(gameContainer.time)
        gameContainer.add_widget(opTeamText)
        gameContainer.add_widget(gameContainer.yourTeamScore)
        gameContainer.add_widget(dash)
        gameContainer.add_widget(gameContainer.opTeamScore)

        # Add layout to gameContainers list and to grid
        self.gameContainers.append(gameContainer)
        self.grid.add_widget(gameContainer)
        return

    # This function can be handled by the child thread
    #def updateGames(self):
        #this will run when a game is made, and will run till no games exist
        #this is where game handler will be stored?
     #   if (debug):
      #      print("How Many Games: ")
       #     print(len(self.gamehandler.games))
        #while(len(self.gamehandler.games)):
         #   for game in self.gamehandler.games:
          #      if(debug):
           #         print("Creating temp game!")

                #self.gameContainers[0].yourTeamScore.text = game.myScore
                #self.gameContainers[0].children["3"].text = "3"
                #game.myTeam
                #game.myScore
                #game.opTeam
                #game.opScore
                #game.time
                # I can call this on everything (Used for lights section of project (to come))
                #game.updated[updateFlags.MYTEAMSCORED]
            #gameHandler.sleep(60)
        #return


    # This function should be added to the kivy scheduler to be called every minute
    def updateScreen(self):
        games = self.gamehandler.returnGames()
        for i in range(len(games)):

            # Need to str cast these ints
            self.gameContainers[i].yourTeamScore.text = str(games[i].myScore)
            self.gameContainers[i].opTeamScore.text = str(games[i].opScore)
            self.gameContainers[i].time.text = games[i].time
            print(games[i].time)
            print(self.gameContainers[i])
        print("Been a minute!")

        return


def main():
    appDisplay().run()

if __name__ == "__main__":
    main()
