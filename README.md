# PiTeamLights
This program uses a Google data scraper to find the live scores of team based sports events
This program runs in three parts
Part 1 - The Data Scrapper
  Using BeautySoup, the python library, I created a GameHandler class which stores the live scores for said sport events, and scrapes google every minute for any changes to the score. The DataHandler uses threading to run updating functions concurrently so the program can constantly listen for user input on adding more games while still updating the games currently set to be checked
  
  Part 2 - The Display
    The display function implements the Kivy library for Python. I chose Kivy because I wish to eventualy run this function on a raspberry Pi, and Kivy is a very versitile library supported by multiple applications. The display function doubles as the main function for now, but I do wish to implement a seperate main function once I finish part 3 of the project. The display function stores the GameHandler, and checks the gameHandler object every minute for any changes in the live score. The display class will also be used to call the lights function once that part is implemented.
    
Part 3 - The Lights
    This part of the project will be where the colors of the team flashes when said team scores. I will need to do more research into what library would best help with this part of the project. I am waiting on a breadbox and programmable lights before I spend too much time on this part of the project
