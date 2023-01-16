import json
import LevelsManager, character

numLeds = 300         
N = 200_000
framerate = 30
characters = []
   
def Init():
    LevelsManager.Init(numLeds, framerate)
    character1 = character.Character()
    character2 = character.Character()
    characters.append(character1)
    characters.append(character2)
    #explotionsManager = new ExplotionsManager();
    
Init()