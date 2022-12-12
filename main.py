from Visualization import *


numberPlayers = SelectScreen.SelectPlayerScreen()

MapSize = SelectScreen.SelectLevelScreen()
if MapSize <5: winCondition = 3
elif MapSize == 5: winCondition = 4
else: winCondition = 5

if (numberPlayers==1): Algo =SelectScreen.SelectAlgorithmScreen()
else: Algo = "none"


while True:
    Map = [[0 for _ in range(MapSize)] for _ in range(MapSize)]
    toast = Visualization(Map, winCondition, numberPlayers, Algo).Display()
    if toast != "Play again": break