# I am going to use Kivy to do the display bc it offers beutiful design
# and seems very capatable when it comes to working on the raspberry Pi and even
# gives me the option to export to android in the future if I wish (prob pay for API access
# before I decide to export to android)

#This code is following a tutorial by Python Simplified on YT https://youtu.be/YDp73WjNISc

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
import gameHandler
from functools import partial

class SayHello(App):
    def build(self):
        self.window = BoxLayout()
        self.window.orientation = "vertical"
        self.grid = GridLayout()
        self.grid.cols = 2
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
        self.button.bind(on_press=self.callback)
        self.window.add_widget(self.button)
        self.grid.add_widget(Image(source = "disgust_bird.jpg"))
        self.greeting = Label(
                        text="Hello World!",
                        font_size = 18,
                        color="#00FFCE"
                        )
        self.grid.add_widget(self.greeting)
        self.user = TextInput(
                    multiline=False,
                    padding_y = (20,20),
                    size_hint=(1, 0.5)
                    )

        self.grid.add_widget(self.user)

        self.window.add_widget(self.grid)

        return self.window

    def callback(self, instance):
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
        #buttonCallBack = lambda yourTeam, opTeam: self.addGameToScreen(yourTeam, opTeam)
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

    def addGameToScreen(self, instance):
        gameHandler.addingGame(self.yourTeam.text, self.opTeam.text)
        self.addGame.dismiss()
        return

def main():
    SayHello().run()


main()
