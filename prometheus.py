"""
Prometheus: Text-Based Game
A person stuck on an island who has to complete tasks in order to get off of it.
"""
import random
import json #https://stackabuse.com/reading-and-writing-json-to-a-file-in-python/
from os import path #https://www.guru99.com/python-check-if-file-exists.html

heroXp = 50
wolfXp = -30
fireXp = -25
treasureXp = 20
collectedTreasures = 0
level = 1
kills = 0
runLimit = 0
wolves = []
fires = []
treasures = []
loadedGame = False
heroName = ''

maxMapSize = 3
heroLocation = [maxMapSize//2, maxMapSize//2]
moveCount = 0

#Functions
def placeWolves(heroLocation, number):
  """
  Randomly places wolves on the map, where the hero is not located
  """
  wolvesLocations = []
  wolfLocation = [random.randrange(0, maxMapSize), random.randrange(0, maxMapSize)]
  count = 0

  #This will ensure that a wolf is not placed on a space with the hero or another wolf
  while count < number:
    while wolfLocation == heroLocation or wolfLocation in heroLocation or wolfLocation in wolvesLocations:
      wolfLocation = [random.randrange(0, maxMapSize), random.randrange(0, maxMapSize)]

    wolvesLocations.append(wolfLocation)
    count += 1

  return wolvesLocations

def placeFires(heroLocation, wolves, number):
  """
  Randomly places fires on the map, where the hero or wolves are not located
  """
  fireLocations = []
  fireLocation = [random.randrange(0, maxMapSize), random.randrange(0, maxMapSize)]
  count = 0

  #This will ensure that a fire is not placed on a space with the hero, a wolf or a fire
  while count < number:
    while fireLocations == heroLocation or fireLocations in heroLocation or fireLocation in wolves or fireLocation in fireLocations:
        fireLocation = [random.randrange(0, maxMapSize), random.randrange(0, maxMapSize)]

    fireLocations.append(fireLocation)
    count += 1

  return fireLocations

def placeTreasures(heroLocation, number):
  """
  Randomly places treasures on the map, where the hero is not located
  """
  treasureLocations = []
  treasureLocation = [random.randrange(0, maxMapSize), random.randrange(0, maxMapSize)]
  count = 0

  #This will ensure that a treasure is not placed on a space with the hero or treasure
  while count < number:
    while treasureLocation == heroLocation or treasureLocation in treasureLocations:
      treasureLocation = [random.randrange(0, maxMapSize), random.randrange(0, maxMapSize)]

    treasureLocations.append(treasureLocation)
    count += 1

  return treasureLocations

def printHeroData():
  """
  Prints hero's data
  """
  global heroXp, heroLocation, collectedTreasures, level, kills, heroName

  print(heroName)
  print('XP:', heroXp)
  print(f'Location: {heroLocation[0]}, {heroLocation[1]}')
  print(f'Treasures: {collectedTreasures}')
  print(f'Kills: {kills}')
  if (level >= 3) : print(f'Runs Left: {3 - runLimit}')
  print(f'Current Level: {level}')

  #Move on to the next level after fires and wolves have been fought
  if (len(wolves) == 0 and len(fires) == 0):
    nextLevel()
  else:
    validateInput('\n1. UP \n2. DOWN \n3. LEFT \n4. RIGHT \n5. SAVE \n6. LOAD \n99. EXIT \n')

def moveHero(move):
  """
  Moves hero around the map
  """
  global heroLocation, moveCount

  #Determine the input to determine the next move
  if (move == 1):
    moveUp = heroLocation[1] - 1
    if (moveUp < 0):
      validateInput('Sorry not valid move! Please try 2, 3 or 4: ')
    else:
      newPosition =[heroLocation[0], moveUp] 
      danger = checkForDanger(newPosition)

      if (not danger[0] or danger[1]):
        heroLocation[1] = moveUp

      collectTreasure()

  elif (move == 2):
    moveDown = heroLocation[1] + 1
    if (moveDown >= maxMapSize):
      validateInput('Sorry not valid move! Please try 1, 3 or 4: ')
    else:
      newPosition =[heroLocation[0], moveDown] 
      danger = checkForDanger(newPosition)

      if (not danger[0] or danger[1]):
        heroLocation[1] = moveDown

      collectTreasure()

  elif (move == 3):
    moveLeft = heroLocation[0] - 1
    if (moveLeft < 0):
      validateInput('Sorry not valid move! Please try 1, 2 or 4: ')
    else:     
      newPosition = [moveLeft, heroLocation[1]]
      danger = checkForDanger(newPosition)

      if (not danger[0] or danger[1]):
        heroLocation[0] = moveLeft

      collectTreasure()

  elif (move == 4):
    moveRight = heroLocation[0] + 1
    if (moveRight >= maxMapSize):
      validateInput('Sorry not valid move! Please try 1, 2 or 4: ')
    else:
      newPosition = [moveRight, heroLocation[1]]
      danger = checkForDanger(newPosition)

      if (not danger[0] or danger[1]):
        heroLocation[0] = moveRight

      collectTreasure()

  elif (move == 5):
    saveGame(False)

  elif (move == 6):
    loadGame()

  elif (move == 99):
    if (moveCount > 0):
      try:
        save = int(input('Do you want to save the game? (This will overwrite any exisiting saved game) \n1. YES \n2. NO \n'))
        if (save == 1):
          saveGame(True)
        else:
          exit()
      except SystemExit:
        exit()      
      except SystemError:
        print('Game not saved! Please enter a valid number \n')

    else:
      exit()

  else:
    validateInput('Sorry not valid move! Please try 1, 2, 3 or 4: ')

  if (move in range(1, 5)) : moveCount += 1
  printHeroData()
  
def collectTreasure():
  """
  The hero collects the treasure
  """
  global heroXp, heroLocation, collectedTreasures

  if heroLocation in treasures:
    heroXp += treasureXp
    collectedTreasures += 1
    treasures.remove(heroLocation)

    print(f'You found treasure and gained {treasureXp} XP!')

def checkForDanger(newPosition):
  """
  The hero checks for danger
  """
  global wolfXp, fireXp, wolves, fires

  if newPosition in wolves:
    print("DANGER! WOLF! \n")
    encountered = encounterDanger(wolfXp, newPosition)

    return [True, encountered]

  elif newPosition in fires:
    print("DANGER! FIRE! \n")
    encountered = encounterDanger(fireXp, newPosition)

    return [True, encountered]

  return [False, False]

def encounterDanger(dangerXp, location):
  """
  The hero encouters danger
  """
  global heroXp, wolves, fires, runLimit, heroLocation, kills, wolfXp, fireXp

  takenLocations = []
  takenLocations.append(location)
  takenLocations.append(heroLocation)

  if (runLimit >= 3):
    print("You cannot run anymore! You have to fight!")
    encounter = 2
  else:
    encounter = int(input("Do you want to run or fight? \n1. RUN \n2. FIGHT \n"))

  if (encounter == 1):
    if (dangerXp == wolfXp):
      runLimit += 1

      if (level >= 3):
        for wolf in wolves:
          takenLocations.append(wolf)

        placeWolves(takenLocations, 1)
        wolves.remove(location)

    return False

  heroXp += dangerXp

  if (heroXp <= 0):
    print('Game Over! New game starting!')
    startGame()
  else:
    print(f'Danger defeated! {-1 * dangerXp} XP lost!')
    kills += 1
    
    if (dangerXp == wolfXp):
      if location in wolves:
        wolves.remove(location)
    elif (dangerXp == fireXp):
      if location in fires:
        fires.remove(location)

  return True

def startGame():
  """
  Resets the game variable for new game
  """
  global heroXp, wolves, fires, treasures, maxMapSize, heroLocation, collectedTreasures, level, runLimit, kills, moveCount, heroName

  heroName = input('What is your hero\'s name?: ')
  heroXp = 50
  collectedTreasures = 0
  level = 1
  runLimit = 0
  kills = 0
  moveCount = 0

  wolves = placeWolves(heroLocation, 1)
  fires = placeFires(heroLocation, wolves, 1)
  treasures = placeTreasures(heroLocation, 2)
  
  maxMapSize = 3
  heroLocation = [maxMapSize//2, maxMapSize//2]

  makeMove('')

def nextLevel():
  """
  Advances hero to next level
  """
  global level, wolves, fires, treasures, heroLocation, runLimit, treasures, maxMapSize

  level += 1
  runLimit = 0
  number = 2 * level
  
  wolves = placeWolves(heroLocation, number)
  fires = placeFires(heroLocation, wolves, number)
  treasures = placeTreasures(heroLocation, number)

  maxMapSize = number + 1
  heroLocation = [maxMapSize//2, maxMapSize//2]

  if (level >= 5):
    print(f'Well done, {heroName}! You have won with:')
    print(f'XP: {heroXp}')
    print(f'Kills: {kills}')
    print(f'Treasures: {collectedTreasures}')
    deleteSavedGame()
    initialiseGame()

  else:
    print(f'Well done, {heroName}! You have completed level {level - 1}. You are now on level {level}.')
    print('Level Summary:')
    print(f'XP: {heroXp}')
    print(f'Kills: {kills}')
    print(f'Treasures: {collectedTreasures}')
    print(f'Location: {heroLocation}')

    makeMove('')

def loadGame():
  """
  Load saved game
  """
  global heroXp, wolfXp, fireXp, treasureXp, collectedTreasures, level, runLimit, wolves, fires, treasures, maxMapSize, heroLocation, kills, loadedGame, moveCount, heroName

  if (not path.exists('saved_game.json')):
    makeMove('No saved game data')

  with open('saved_game.json', 'r') as savedGame:
    gameData = json.load(savedGame)

    if (len(gameData) == 0):
      makeMove('No saved game data')

    heroName = gameData['heroName']
    heroXp = gameData['heroXp']
    wolfXp = gameData['wolfXp']
    fireXp = gameData['fireXp']
    treasureXp = gameData['treasureXp']
    collectedTreasures = gameData['collectedTreasures']
    level = gameData['level']
    runLimit = gameData['runLimit']
    wolves = gameData['wolves']
    fires = gameData['fires']
    treasures = gameData['treasures']
    maxMapSize = gameData['maxMapSize']
    heroLocation = gameData['heroLocation']
    kills = gameData['kills']
    moveCount = gameData['moveCount']

    loadedGame = True
    savedGame.close()

  makeMove('Saved Game loaded!')

def saveGame(exitGame):
  """
  Save game
  """
  global heroXp, wolfXp, fireXp, treasureXp, collectedTreasures, level, runLimit, wolves, fires, treasures, maxMapSize, heroLocation, kills, moveCount, heroName

  gameData = {
    'heroName': heroName,
    'heroXp': heroXp,
    'wolfXp': wolfXp,
    'fireXp': fireXp,
    'treasureXp': treasureXp,
    'collectedTreasures': collectedTreasures,
    'level': level,
    'runLimit': runLimit,
    'wolves': wolves,
    'fires': fires,
    'treasures': treasures,
    'maxMapSize': maxMapSize,
    'heroLocation': heroLocation,
    'kills': kills,
    'moveCount': moveCount
  }

  with open('saved_game.json', 'w') as savedGame:
    json.dump(gameData, savedGame)
    savedGame.close()

  message = 'Game saved!'
  if (exitGame):
    print(message)
    exit(0)
  else:
    makeMove(message)

def deleteSavedGame():
  """
  Delete saved game data
  """
  global loadedGame

  if (loadedGame):
    gameData = ''

    with open('saved_game.json', 'w') as savedGame:
      json.dump(gameData, savedGame)

      loadedGame = False
      savedGame.close()

def makeMove(message):
  print(message)
  move = int(input('\nMake your move!\n\n1. UP \n2. DOWN \n3. LEFT \n4. RIGHT \n5. SAVE \n6. LOAD \n99. EXIT \n'))
  moveHero(move)

def validateInput(message):
  try:
    moveHero(int(input(message)))
  except SystemExit:
    exit()
  except:
    print('Please enter a valid number \n')
    moveHero(int(input(message)))
  
def initialiseGame():
  """
  Prompt a user to either start a new game or load an existing one
  """
  
  print('“Prometheus”, a person stuck on an island who has to complete tasks in order to get off of it. \n')
 
  try:
  	startAGame = int(input('Start a new game or load a saved game? \n1. NEW \n2. LOAD \n99. EXIT \n'))
  	if (startAGame == 1):
  	  startGame()
  	elif (startAGame == 2):
  	  loadGame()
  	elif (startAGame == 99):
  	  exit() 
  	else:
  	  print('Please enter 1, 2 or 99')
  	  initialiseGame()
  except SystemExit:
  	exit() 
  except:
  	print('Please enter a valid number \n')
  	initialiseGame()

#Start Game
initialiseGame()