from config import dictionaryloc
from config import turntextloc
from config import wheeltextloc
from config import maxrounds
from config import vowelcost
from config import roundstatusloc
from config import finalprize
from config import finalRoundTextLoc

import random

players={0:{"roundtotal":0,"gametotal":0,"name":""},
         1:{"roundtotal":0,"gametotal":0,"name":""},
         2:{"roundtotal":0,"gametotal":0,"name":""},
        }

roundNum = 0
dictionary = []
turntext = ""
wheellist = []
roundWord = ""
blankWord = []
vowels = {"A", "E", "I", "O", "U"}
roundstatus = ""
finalroundtext = ""

def readDictionaryFile():
    global dictionary
    # Read dictionary file in from dictionary file location
    f = open(dictionaryloc, 'r')
    dictionary = f.read().splitlines()
    f.close()
    # Store each word in a list.

def readTurnTxtFile():
    global turntext   
    #read in turn intial turn status "message" from file
    f = open(turntextloc, 'r')
    turntext = f.read()
    f.close()

def readFinalRoundTxtFile():
    global finalroundtext   
    #read in turn intial turn status "message" from file
    f = open(finalRoundTextLoc, 'r')
    finalroundtext = f.read()
    f.close()

def readRoundStatusTxtFile():
    global roundstatus
    # read the round status  the Config roundstatusloc file location
    f = open(roundstatusloc, 'r')
    roundstatus = f.read()
    f.close()

def readWheelTxtFile():
    global wheellist
    # read the Wheel name from input using the Config wheelloc file location
    f = open(wheeltextloc, 'r')
    wheellist = f.read().splitlines()
    f.close()

def getPlayerInfo():
    global players
    # read in player names from command prompt input
    player0 = str(input('Type in a name for player 0: '))
    player1 = str(input('Type in a name for player 1: '))
    player2 = str(input('Type in a name for player 2: '))
    # update players dict to include player names
    players[0].update({'name':f'{player0}'})
    players[1].update({'name':f'{player1}'})
    players[2].update({'name':f'{player2}'})

def gameSetup():
    # Read in File dictionary
    # Read in Turn Text Files
    global turntext
    global dictionary
        
    readDictionaryFile()
    readTurnTxtFile()
    readWheelTxtFile()
    getPlayerInfo()
    readRoundStatusTxtFile()
    readFinalRoundTxtFile()

def getWord():
    global dictionary
    #choose random word from dictionary
    roundWord = random.choice(dictionary).upper()
    #make a list of the word with underscores instead of letters.
    roundUnderscoreWord = '_'.rjust(len(roundWord), '_')
    return roundWord,roundUnderscoreWord

def wofRoundSetup():
    global players
    global roundWord
    global blankWord
    # Set round total for each player = 0
    players[0].update({'roundtotal':0})
    players[1].update({'roundtotal':0})
    players[2].update({'roundtotal':0})    
    # Return the starting player number (random)
    initPlayer = random.randint(min(players.keys()), max(players.keys()))
    # Use getWord function to retrieve the word and the underscore word (blankWord)
    roundWord, blankWord = getWord()

    return initPlayer

def spinWheel(playerNum):
    global wheellist
    global players
    global vowels

    # Get random value from wheellist
    spin_result = random.choice(wheellist)
    # Check for bankrupcy, and take action.
    if spin_result == 'BANKRUPT':
        print(f'Oh no, you landed on {spin_result}')
        players[playerNum].update({'roundtotal':0})
        stillinTurn = False
    # Check for loose turn
    elif spin_result == 'LOSE A TURN':
        print(f'You landed on {spin_result}')
        stillinTurn = False
    # Get amount from wheel if not loose turn or bankruptcy
    else:
        amount = int(spin_result)
        # Ask user for consonant letter guess
        guess_is_vowel = True
        while guess_is_vowel:
            letter_guess = str(input(f'Enter your consonant guess for {amount} dollars: ')).upper()
            # ensure letter is a consonant.
            if letter_guess in vowels:
                print('Your guess must be a consonant. Please try again')
            elif letter_guess not in vowels:
                guess_is_vowel = False
        # Use guessletter function to see if guess is in word, and return count
        goodGuess, count = guessletter(letter_guess, playerNum)
        # Change player round total if they guess right.
        if goodGuess == True:
            current_roundtotal = players[playerNum]['roundtotal']
            new_roundtotal = current_roundtotal + amount
            players[playerNum].update({'roundtotal':new_roundtotal})
            stillinTurn = True
        elif goodGuess == False:
            stillinTurn = False
    return stillinTurn

def find_char_index(word, character):
    indices = []
    for i in range(len(word)):
        if character == word[i]:
            indices.append(i)
    return indices

def remainingLetters(word2guess, word_w_blanks):
    letters_left = []
    for i in range(len(word2guess)):
        if word2guess[i] != word_w_blanks[i]:
            letters_left.append(word2guess[i])
    return letters_left

def guessletter(letter, playerNum): 
    global players
    global blankWord
    global roundWord
    # parameters:  take in a letter guess and player number
    # Change position of found letter in blankWord to the letter instead of underscore
    indices = find_char_index(roundWord, letter)
    if len(indices) > 0:
        blankWord = list(blankWord)
        for index in indices:
            blankWord[index] = letter
        blankWord = "".join(blankWord)
        # return goodGuess= true if it was a correct guess
        goodGuess = True
    else:
        goodGuess = False
    
    # return count of letters in word.
    count = len(indices)
    print(f'{letter} occurs {count} times in {blankWord}')
    
    return goodGuess, count

def buyVowel(playerNum):
    global players
    global vowels
    
    # Take in a player number
    # Ask user for vowel letter guess
    guess_is_consonant = True
    while guess_is_consonant:
        letter_guess = str(input('Which vowel would you like to purchase: ')).upper()
        # ensure letter is a vowel.
        if letter_guess not in vowels:
            print('Your letter must be a vowel. Please try again')
        elif letter_guess in vowels:
            guess_is_consonant = False
        
    # Use guessLetter function to see if the letter is in the roundword
    goodGuess, count = guessletter(letter_guess, playerNum)
    
    return goodGuess

def guessWord(playerNum):
    global players
    global blankWord
    global roundWord
    
    # Take in player number
    # Ask for input of the word and check if it is the same as wordguess
    player_guess = str(input('Enter your guess: ')).upper()
    # Fill in blankWord with all letters, instead of underscores if correct
    if player_guess == roundWord:
        blankWord = roundWord
        #Add roundtotal to gametotal
        roundtotal = players[playerNum]['roundtotal']
        gametotal = players[playerNum]['gametotal']
        new_gametotal = gametotal + roundtotal
        players[playerNum].update({'gametotal':new_gametotal})
        print(f'Correct, the word is {blankWord}')
    else:
        print('That is not the correct word')
    # return False ( to indicate the turn will finish)  
    
    return False

def wofTurn(playerNum):  
    global roundWord
    global blankWord
    global turntext
    global players

    # take in a player number. 
    # use the string.format method to output your status for the round
    print(roundstatus.format(
        curr_round = roundNum, player0name = players[0]['name'], p0rt = players[0]['roundtotal'],
        p0gt = players[0]['gametotal'], player1name = players[1]['name'], p1rt = players[1]['roundtotal'],
        p1gt = players[1]['gametotal'], player2name = players[2]['name'], p2rt = players[2]['roundtotal'],
        p2gt = players[2]['gametotal'])
         )

    current_player = players[playerNum]['name']
        
    # Keep doing all turn activity for a player until they guess wrong
    # Do all turn related activity including update roundtotal 
    
    stillinRound = True
    stillinTurn = True
    turnnum = 0
    while stillinTurn:
        # use the string.format method to output your status for the round
        roundtotal = players[playerNum]['roundtotal']
        print(turntext.format(player = players[playerNum]['name'], roundmoney = roundtotal, word2guess=blankWord))
        #Gather letters left to check if remaining letters are all vowels
        letters_left = remainingLetters(roundWord, blankWord)
        
        #Ask to (s)pin the wheel or G(uess) the word at the start of turn (vowel after succesful consonant guess)
        if turnnum == 0:
            choice = str(input(f'{current_player} (S)pin the wheel or (G)uess the word (S/G)?: ')).upper()
            while choice not in ['S', 'G']:
                print("Not a correct option")
                choice = str(input(f'{current_player} (S)pin the wheel or (G)uess the word (S/G)?: ')).upper()
        
        #Check if remaining letters are all vowels
        elif all([letter not in vowels for letter in letters_left]):
            print('No more vowels left')
            choice = str(input(f'{current_player} (S)pin the wheel or (G)uess the word (S/G)?: ')).upper()
            while choice not in ['S', 'G']:
                print("Not a correct option")
                choice = str(input(f'{current_player} (S)pin the wheel or (G)uess the word (S/G)?: ')).upper()
                
        #Check if no more vowels
        elif all([letter in vowels for letter in letters_left]):
            print('Only vowels left')
            choice = str(input(f'{current_player} (B)uy vowel or (G)uess the word (B/G)?: ')).upper()
            while choice not in ['B', 'G']:
                print("Not a correct option")
                choice = str(input(f'{current_player} (B)uy vowel or (G)uess the word (B/G)?: ')).upper() 
            
        else:
            # and Ask to (s)pin the wheel, (b)uy vowel, or G(uess) the word using
            #current_player = players[playerNum]['name']
            choice = str(input(f'{current_player} (S)pin the wheel, (B)uy vowel, or (G)uess the word (S/B/G)?: ')).upper()
    
        if(choice.strip().upper() == "S"):
            stillinTurn = spinWheel(playerNum)
        elif(choice.strip().upper() == "B"):
            # Ensure player has 250 for buying a vowelcost
            current_roundtotal = players[playerNum]['roundtotal']
            if current_roundtotal >= vowelcost:
                new_roundtotal = current_roundtotal - vowelcost
                players[playerNum].update({'roundtotal':new_roundtotal})
                stillinTurn = buyVowel(playerNum)
            elif current_roundtotal < 250:
                print('You do not have enough to buy a vowel Choose another option.')
                stillinTurn = True
        elif(choice.strip().upper() == "G"):
            stillinTurn = guessWord(playerNum)
        else:
            print("Not a correct option")
        
        turnnum += 1
        # Check to see if the word is solved, and change stillinTurn to false if it is,
        if blankWord == roundWord:
            stillinTurn = False
            stillinRound = False
    # Or otherwise break the while loop of the turn.
    else:
        stillinTurn = False
    return stillinRound

def wofRound(thisround):
    global players
    global roundWord
    global blankWord
    global roundstatus
    global roundNum
    roundNum = thisround
    initPlayer = wofRoundSetup()
    
    # Keep doing things in a round until the round is done ( word is solved)
    stillinRound = True
    # While still in the round keep rotating through players
    playerNum = initPlayer - 1
    while stillinRound:
        playerNum = (playerNum + 1) if (playerNum + 1) <= 2 else 0
        
        # Use the wofTurn fuction to dive into each players turn until their turn is done.
        stillinRound = wofTurn(playerNum)
    
    # Print roundstatus with string.format, tell people the state of the round as you are leaving a round.
    print(roundstatus.format(
        curr_round = roundNum, player0name = players[0]['name'], p0rt = players[0]['roundtotal'],
        p0gt = players[0]['gametotal'], player1name = players[1]['name'], p1rt = players[1]['roundtotal'],
        p1gt = players[1]['gametotal'], player2name = players[2]['name'], p2rt = players[2]['roundtotal'],
        p2gt = players[2]['gametotal'])
         )

def wofFinalRound():
    global roundWord
    global blankWord
    global finalroundtext
    winplayer = 0
    amount = 0
    
    # Find highest gametotal player.  They are playing.
    gametotals = []

    for i in range(len(players.keys())):
        gametotals.append(players[i]['gametotal'])
    for i in range(len(gametotals)):
        if players[i]['gametotal'] == max(gametotals):
            winplayer = i
            
    # Print out instructions for that player and who the player is.
    print(finalroundtext.format(winner = players[winplayer]['name'], cashprize = finalprize))
    # Use the getWord function to reset the roundWord and the blankWord ( word with the underscores)
    roundWord, blankWord = getWord()
    # Use the guessletter function to check for {'R','S','T','L','N','E'}
    given_letters = ['R', 'S', 'T', 'L', 'N', 'E']
    for letter in given_letters:
        guessletter(letter, winplayer)
    # Print out the current blankWord with whats in it after applying {'R','S','T','L','N','E'}
    print(blankWord)
    # Gather 3 consonants and use the guessletter function to see if they are in the word
    user_consonants = []
    for i in range(3):
        user_consonant = str(input('Enter a consanant: ')).upper()
        while user_consonant in vowels:
            print('That is not a consonant. Please try again.')
            user_consonant = str(input('Enter a consanant: ')).upper()
        user_consonants.append(user_consonant)
    for consonant in user_consonants:
        guessletter(consonant, winplayer)
    #Gather 1 vowel and use guessletter function to see if they are in the word
    user_vowel = str(input('Enter a vowel: ')).upper()
    while user_vowel not in vowels:
        print('That is not a vowel. Please try again.')
        user_vowel = str(input('Enter a vowel: ')).upper()
    guessletter(user_vowel, winplayer)
    # Print out the current blankWord again
    print(blankWord)
    # Remember guessletter should fill in the letters with the positions in blankWord
    # Get user to guess word
    player_guess = str(input('Enter your guess: ')).upper()
    # If they do, add finalprize and gametotal and print out that the player won
    gametotal = players[winplayer]['gametotal']
    if player_guess == roundWord:
        prizemoney = finalprize + gametotal
        winning_player = players[winplayer]['name']
        print(f'Congrats! {winning_player} has won {prizemoney} dollars.')
    elif blankWord != roundWord:
        print(f'No, the correct answer was {roundWord}. You lose, but you still take home {gametotal}')


def main():
    gameSetup()    

    for i in range(0,maxrounds):
        if i in [0,1]:
            wofRound(i)
        else:
            wofFinalRound()

if __name__ == "__main__":
    main()