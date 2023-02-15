from fileinput import filename
import os
import math
import random

class Game():
    dictionary = []
    def __init__(self, debug):
        if debug != "D":
            self.dictionary = self.readFile('dictionary.txt')
        else:
            self.dictionary = ["ally", "beta", "cool", "deal", "else", "good"]

    def readFile(self, fileName):
        words = []
        __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        file = open(os.path.join(__location__, fileName), 'r')
        words = file.read().split('\n')
        file.close()
        return words

class Player(Game):
    wordLength = 0
    pattern = ""
    wordFamily = dict()
    totalRounds = 0

    def __init__(self, Game):
        # randomly choose the length of the word between 4 and 12
        if len(Game.dictionary) > 6:
            self.wordLength = random.randint(4,12)
        else:
            self.wordLength = 4

        # Total rounds are twice the length of the word
        self.totalRounds = self.wordLength * 2

        # set initial pattern of the word depending on the amount of chars (e.g., _ _ _ _)
        self.pattern = self.setPattern(self.wordLength)

        # set the initial state of the wordFamily
        self.wordFamily = self.setDictionary(Game, self.pattern)

    """
    This functions set the pattern of the current state of the game
    if no previous pattern is provided, then game is in initial state and empty pattern is built
    if previous pattern is provided, then it is updated according to the information provided by the knownLetters dictionartyM
    """
    def setPattern(self, wordLength, knownLetters = None, pattern = ""):
        """
        This dictionary stores the indices of every known letter. Hence, the function knows where
        they need to be placed
        
        knownLetters = {
            'character', [index1, index2] // template
            'A', [1, 3] // example1
            'B', [2] // example2
            ...
        }
        """
        # if there are no known letters, then initial pattern is built
        if knownLetters == None:
            for i in range(wordLength):
                pattern += "_"
        else:
            patternList = list(pattern)

            # Each letter in assigned to their designed index positions
            for letter in knownLetters.keys():
                for index in knownLetters[letter]:
                    patternList[index] = letter
            
            # To ease the process, pattern is treated as a list, but then we would need to return it as a string
            pattern = "".join(patternList)
        return pattern

    """
    This function set the dictionary that contains the word families. It requires the following parameters:
    - Game object to access the main dictionary in case we're in the initial state of the game
    - Pattern of the current state of the game
    - dictionary (optional), if no dictionary (i.e., initial state) it creates an empty one
    - words (optional), if no words then all the words in the Game dictionary are passed
    """
    def setDictionary(self, Game, pattern, dict = {}, words=[]):
        """
        dict = {
            [PATTERN], [ITEMS] 
        }
        """
        # Add every word in the dictionary that satisfies the user game pattern
        
        # when dict is empty, we load all the words from the file
        if not dict:
            for word in Game.dictionary:
                # the length of the word is random, so we only need those words that match with that length
                if self.isValidPattern(word, pattern):
                    dict.setdefault(pattern, []).append(word)
        else:
            for word in words:
                if self.isValidPattern(word, pattern):
                    dict.setdefault(pattern, []).append(word)
        return dict
    
    def getWordFamilies(self):
        for key in self.wordFamily.keys():
            print(f"[{key}]: {self.wordFamily[key]}")
    """
    This functions take as a parameter a word, and a pattern and returns a boolean value that expresses whether
    the pattern matches the word (e.g., "HOUSE" and "H _ _ S E" would return True)
    """
    def isValidPattern(self, word, pattern):
        for i in range(0, len(word)):
            """
            word is not valid if:
             - word and pattern do not have the same length OR
             - pattern's letter at i position is a proper letter (i.e., not '_'), AND it is different from word's letter at i position 
             - patter's letter at i position matches with the word's letter at i position, BUT the occurrences of that letter are different, this is
               to avoid prevent false matches like "word: ABABA and pattern: A _ A _ _ ". Indeed a valid pattern for that word would be: "A_A_A".
            """
            if len(word) != len(pattern) or word[i] != pattern[i] and pattern[i] != "_" or word[i] == pattern[i] and word.count(word[i]) != pattern.count(word[i]):
                return False
        return True
    
    """
    This function simply returns a boolean value that expresses whether the letter is in the word pattern
    """
    def isNotInPattern(self, letter, pattern):
        return letter not in list(pattern)

    """
    This function is responsible for choosing the word family by considering the difficulty level of the Game passed as parameter
    - if EASY, it simply choose the wordFamily that has more available words
    - if HARD, it assigns a weights to all the word families available and choose the one with highest weight
    """
    def chooseWordFamily(self, difficulty, debug=""):
        chosenFamily = ""
        newDict = {}

        if difficulty == 'E':
            wordCounter = 0
            # when the difficulty is set to 0, the family with more words is chosen
            for key in self.wordFamily.keys():
                if wordCounter < len(self.wordFamily[key]):
                    wordCounter = len(self.wordFamily[key])
                    chosenFamily = key
        else:
            # first of all the program ask himself if we are in the terminal state i.e., the player guessed the word
            if not self.terminalState():
                    # if not, all word families are assigned a weight, and the one with the highest weight is chosen
                    highestWeight = 0
                    weights = self.setWeights()
                    for key in weights.keys():
                        if weights[key] == 100:
                            chosenFamily = key
                            break
                        elif highestWeight < weights[key]:
                            highestWeight = weights[key]
                            chosenFamily = key
                    if debug == "D":
                        print("Assigned weights:")
                        for key in weights.keys():
                            print(f"[{key}]: [{weights[key]}]")
            else:
                chosenFamily = list(self.wordFamily.keys())[1]
    
        newDict[chosenFamily] = self.wordFamily[chosenFamily]
        self.wordFamily = newDict
        self.pattern = chosenFamily

    """
    This function returns a boolean value that expresses whether the terminal state has been reached
    In other words, if the user won the game
    """
    def terminalState(self):
        for key in self.wordFamily.keys():
            # Checks all the patterns and returns True as soon as a pattern without letters to discover is found
            if self.isNotInPattern('_', key):
                return True
        return False
    
    """
    This function is responsible for assigning weight for each font family
    The logic is that there are three important factor to consider when choosing a wordFamily:
        - The amount of words a word Family has (~ worth 60%)
        - The amount of undiscovered words the pattern has (~ worth 30%)
        - The maximum number of possible letters that are required to guess the word (~ 10%)
    """
    def setWeights(self):
        weights = {}
        for key in self.wordFamily.keys():
            weights[key] = 0
        
        # first factor is calculated
        maxItems = self.getMaximumNumberOfWords()
        weights = self.setWordFamilyWeight(maxItems, weights)
        
        # second factor is calculated
        maxOccurrences = self.getMaxUndiscoveredLetters()
        weights = self.setMaxUndiscoveredWeight(maxOccurrences, weights)

        # third factor is calculated
        possibleLetters, maxPossibleLetters = self.getMaxNumOfPossibleLetters()
        weights = self.setMaxNumOfPossibleLettersWeight(maxPossibleLetters, possibleLetters, weights)
        return weights

    """
    This function returns the maximum number of words found in one of the word families
    This value will be used as a point of reference to calculate the weights for all the other families
    """
    def getMaximumNumberOfWords(self):
        maxItems = 0
        for key in self.wordFamily.keys():
            if len(self.wordFamily[key]) > maxItems:
                maxItems = len(self.wordFamily[key])
        return maxItems

    """
    This function takes the maximum number of words found in one of the word families, and calculates the 
    weight of all the word families in the current state
    """
    def setWordFamilyWeight(self, maxItems, weights):
        for key in weights:
            # 60/100 is the maximum weight this factor can have
            weights[key] = (len(self.wordFamily[key]) * 60) / maxItems
        return weights

    """
    This function returns the maximum number of undiscovered letters found in one of the word families (i.e., less letters are known, the better it is)
    This value will be used as a point of reference to calculate the weights for all the other families
    """
    def getMaxUndiscoveredLetters(self):
        maxOccurrence = 0
        for key in self.wordFamily.keys():
            if str(key).count('_') > maxOccurrence:
                maxOccurrence = str(key).count('_')
        return maxOccurrence

    """
    This function takes the maximum number of undiscovered letters found in one of the word families, and calculates the 
    weight of all the word families in the current state
    """
    def setMaxUndiscoveredWeight(self, maxOccurrence, weights):
        for key in weights:
            # 30/100 is the maximum weight this factor can have
            weights[key] += (str(key).count('_') * 30) / maxOccurrence
        return weights

    """
    This function returns the maximum number of possible letters that can be used to complete the one of the words within a word family (i.e., less letters are known, the better it is)
    This value will be used as a point of reference to calculate the weights for all the other families
    """
    def getMaxNumOfPossibleLetters(self):
        """
        possibleLetters = {
            pattern, [possible letters]
        }
        """
        possibleLetters = dict()
        maxPossibleLetters = 0
        for key in self.wordFamily.keys():
            currentPossibleLetters = set()
            for word in self.wordFamily[key]:
                for letter in list(word):
                        # no need to check for duplicates due to the nature of the set
                        currentPossibleLetters.add(letter)
            # set theory is used to make the algorithm less computational expensive
            currentPossibleLetters = currentPossibleLetters - set(key)
            possibleLetters[key] = currentPossibleLetters
            if maxPossibleLetters < len(currentPossibleLetters):
                maxPossibleLetters = len(currentPossibleLetters)
        # to make the algorithm less computational expensive, this function returns
        #   - a dictionary with all the possible letters for every pattern i.e., word family
        #   - the max number of possible letters within all word families
        return possibleLetters, maxPossibleLetters

    """
    This function exploits the returned values from the getMaxNumOfPossibleLetters function, and assign the weights to the word families
    """
    def setMaxNumOfPossibleLettersWeight(self, maxPossibleLetters, possibleLetters, weights):
        for key in weights:
                # 10/100 is the maximum weight this factor can have
                weights[key] += (len(possibleLetters[key]) * 10) / maxPossibleLetters
        return weights

    """
    This function returns the first word available in the word family
    """
    def chooseWord(self):
        return list(self.wordFamily[self.pattern])[0]

class GuessTheWord():
    def __init__(self, Game, Player):
        round = 1
        discovered_words = set()
        win = False
        while True:
            os.system('clear')
            print("Hello!, and welcome to the Guess the Word game!")
            print("Please, choose the difficulty:")
            difficulty = input(" - Type 'E' for EASY, \n - Type 'H' for HARD\nYour choice: ").upper()
            if difficulty == "E" or difficulty == "H":
                break
        debug = input("Insert 'D' for debug mode, any other keys otherwise: ").upper()

        Game = Game(debug)
        Player = Player(Game)

        while round <= Player.totalRounds and win == False:
            os.system('clear')
            if difficulty == "H":
                print("Mode: HARD")
            else:
                print("Mode: EASY")
            if debug == "D":
                print("Debug Mode: ON")
            print("------------")
            print(f"Word length: {Player.wordLength} letters.")
            print(f"Discovered words: {sorted(discovered_words)}")
            print(f"\nRound {round} of {Player.totalRounds}")
            print("word: " + Player.pattern)
            userLetter = input("Choose a letter: ").lower()
            """
            This code updates dictionary
            """
            if userLetter not in discovered_words and len(userLetter) == 1 and userLetter.isalpha(): 
                discovered_words.add(userLetter)
                if Player.isNotInPattern(userLetter, Player.pattern):
                    words = Player.wordFamily[Player.pattern].copy()
                    for word in words:
                        if userLetter in word:
                            Player.wordFamily[Player.pattern].remove(word)
                            knownLetter = dict()
                            indices = [i for i, x in enumerate(list(word)) if x == userLetter]
                            knownLetter[userLetter] = indices
                            newPattern = Player.setPattern(len(word), knownLetter, Player.pattern)
                            if newPattern not in Player.wordFamily.keys():
                                Player.wordFamily = Player.setDictionary(Game.dictionary, newPattern, Player.wordFamily, words)
                    if debug == "D":
                        print('\n')
                        print("DEBUG MENU")
                        print("------------")
                        print("Available Word Families:")
                        Player.getWordFamilies()
                        print('\n')
                        Player.chooseWordFamily(difficulty, debug)
                        print('\n')
                        print("Chosen Word Family:")
                        Player.getWordFamilies()
                        print('\n')
                        input("Press Enter to continue...")
                    else:
                        Player.chooseWordFamily(difficulty)   
                if Player.isNotInPattern("_", Player.pattern):
                    win = True
                else:
                    round += 1
        os.system('clear')
        if win == True:
            print(f"Congratulations!\nSurprisingly you managed to beat me. The guessed word is '{Player.chooseWord()}', well done!")
        else:
            print(f"Ahah!\nUnfortunately you lost! The word I had in mind was: '{Player.chooseWord()}' ")

GuessTheWord(Game, Player)