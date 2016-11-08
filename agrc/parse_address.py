"""
parse_address
"""

import os
from csv import reader

# reference data
dirs = {
    'N': ['N', 'NORTH', 'NO'],
    'S': ['S', 'SOUTH', 'SO'],
    'E': ['E', 'EAST', 'EA'],
    'W': ['W', 'WEST', 'WE']
}

houseNumSufList = ['1/4', '1/3', '1/2', '2/3', '3/4']

# searching states
searchStates = {
    'houseNumber': 1,
    'houseNumberSuffixOrPrefixDirection': 2,
    'streetName': 3,
    'suffixDirOrType': 4,
    'end': 5
}


class NormalizedAddress:
    houseNumber = None
    houseNumberSuffix = None
    prefixDirection = None
    streetName = None
    suffixType = None
    suffixDirection = None
    normalizedAddressString = None
    originalAddressString = None

    def __init__(self, original):
        self.originalAddressString = original.strip()

    def _getWords(self):
        return self.originalAddressString.upper().split(' ')

    def getPreviousWord(self, word):
        words = self._getWords()
        return words[words.index(word.upper()) - 1]

    def isLastWord(self, word):
        words = self._getWords()
        return words.index(word.upper()) == len(words) - 1


def __getSuffixTypes():
    global reader
    types = {}
    with open(os.path.join(os.path.dirname(__file__), 'data', 'USPS_Street_Suffixes.csv'), 'rb') as file:
        reader = reader(file)
        firstrow = True
        for row in reader:
            if firstrow:
                firstrow = False
                continue
            try:
                types[row[3].strip()].append(row[2].strip())
            except KeyError:
                types[row[3].strip()] = [row[2].strip()]
    return types


def checkWord(word, d):
    for key, value in d.iteritems():
        if word in value:
            return key
    # if nothing is found
    return False


def checkList(word, list):
    if word in list:
        return word
    return False


def parseWord(word, state, add):
    def appendStreetWord(appendWord):
        if add.streetName is None:
            add.streetName.lstrip('0') = appendWord
        else:
            add.streetName += ' {0}'.format(appendWord)

    word = word.replace('.', '')
    if word.strip() == '':
        return state
    if state == searchStates['houseNumber']:
        add.houseNumber.lstrip('0') = word
        return searchStates['houseNumberSuffixOrPrefixDirection']

    elif state == searchStates['houseNumberSuffixOrPrefixDirection']:
        houseNumSuffix = checkList(word, houseNumSufList)
        pDir = checkWord(word, dirs)
        if houseNumSuffix is False and pDir is False:
            appendStreetWord(word)
            return searchStates['suffixDirOrType']
        elif houseNumSuffix is not False:
            add.houseNumberSuffix = houseNumSuffix
            return searchStates['houseNumberSuffixOrPrefixDirection']
        elif pDir is not False:
            add.prefixDirection = pDir
            return searchStates['streetName']

    elif state == searchStates['streetName']:
        sType = checkWord(word, sTypes)
        if sType is not False and add.isLastWord(word):
            appendStreetWord(add.getPreviousWord(word))
            add.prefixDirection = None
            add.suffixType = sType
            return searchStates['end']
        appendStreetWord(word)
        return searchStates['suffixDirOrType']

    elif state == searchStates['suffixDirOrType']:
        sType = checkWord(word, sTypes)
        sDir = checkWord(word, dirs)
        if sType is False and sDir is False:
            appendStreetWord(word)
            return searchStates['suffixDirOrType']
        elif sType is not False:
            add.suffixType = sType
            return searchStates['end']
        else:
            add.suffixDirection = sDir
            return searchStates['end']

    elif state == searchStates['end']:
        sType = checkWord(word, sTypes)
        if sType is not False:
            appendStreetWord(add.getPreviousWord(word))
            add.suffixType = sType
        sDir = checkWord(word, dirs)
        if sDir is not False:
            appendStreetWord(add.getPreviousWord(word))
            add.suffixDirection = sDir
        return searchStates['end']


def parse(address):
    nAdd = NormalizedAddress(address)

    state = searchStates['houseNumber']
    for word in address.strip().split(' '):
        state = parseWord(word.upper(), state, nAdd)

    # Build normalized address string
    if nAdd.suffixType is not None:
        suffixDirOrType = nAdd.suffixType
    elif nAdd.suffixDirection is not None:
        suffixDirOrType = nAdd.suffixDirection
    else:
        suffixDirOrType = ''
    nAdd.normalizedAddressString = nAdd.houseNumber
    if nAdd.prefixDirection is None:
        nAdd.normalizedAddressString += " {0} {1}".format(nAdd.streetName, suffixDirOrType)
    else:
        nAdd.normalizedAddressString += " {0} {1} {2}".format(
            nAdd.prefixDirection, nAdd.streetName, suffixDirOrType)

    nAdd.normalizedAddressString = nAdd.normalizedAddressString.strip()

    return nAdd

sTypes = __getSuffixTypes()
