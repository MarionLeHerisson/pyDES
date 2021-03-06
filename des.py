from constants import *
from resources import *
from ConvAlphaBin import *
import math

## Gets 32 first bits of a 64 bits matrix
# param bloc : size 64 dictionary
# returns size 32 dictionary
def getLeft(bloc):
    G = dict()

    for i in range((len(bloc)//2)): #on est sur 56 et non 64, il faut couper en 28
        G[i] = bloc[i]

    return G


## Gets 32 last bits of a 64 bits matrix
# param bloc : size 64 dictionary
# returns size 32 dictionary
def getRight(bloc):
    D = dict()

    for i in range((len(bloc)//2), len(bloc)):
        D[i - (len(bloc)//2)] = bloc[i]

    return D


## permutes bits of a bloc in accordance to the given matrix
# param bloc : size N dictionary
# param matrix : size N dictionary
# returns size N dictionary
def permute(bloc, matrix):
    newbloc = dict()
    for i in range(len(matrix)):
        newbloc[i] = bloc[matrix[i] - 1]
    return newbloc

def permute54(bloc, matrix):
    newbloc = dict()
    for i in range(len(bloc)-8):
        newbloc[i] = bloc[matrix[i] - 1]
    return newbloc


## Fractions a text from a file in blocs of 64 bits
# param inputFile : string
# yields size 64 dictionaries
def fractionText(inputFile):
    f = open(inputFile, "r")
    content = f.read()
    cursor = 0
    bloc = dict()

    for machin in range(0,math.ceil(len(content)/64)):
        for i in range(0, 64):
            try:
                bloc[i] = content[cursor]
            except:
                bloc[i] = 0
            cursor += 1
        yield bloc

    f.close()


## Removes the parity bits of a 64 bits key
# param key : size 64 string
# returns 56 size string
def convert64to56(key):
    newkey = ""
    i = 0
    for bit in key:
        if (i + 1) % 8 != 0:
            newkey += bit
        i += 1
    return newkey


def shiftKeyBy16(key):
    newKey = ""
    for i in range(0, 16):
        newKey += key[(i + 1) % 16]
    return newKey


def shiftKeyBy8(key):
    newKey = ""
    for i in range(0, len(key)):
        newKey += key[(i+1)% len(key)]
    return newKey

# keys[0] is keys[15], keys[1] is keys[14] and so on
def reverseKeys(keys):
    newKeys = dict()
    for i in range(0,16):
        newKeys[i] = keys[15-i]
    return newKeys


def get16KeysFromKey(key):
    key = permute(key, CP1)
    keys = dict()
    tempG = dictToString(getLeft(key)) # séparer la clé en deux
    tempD = dictToString(getRight(key))
    for i in range(0, 16):
        tempG = shiftKeyBy8(tempG) # shift G
        tempD = shiftKeyBy8(tempD) # shift D
        tempGD = tempG + tempD # concatener G et D
        key = permute54(tempGD, CP2) # permuter GD par CP2
        keys[i] = key
    return keys


#return a dict with 8 strings
def get8BlocsOf6Bits(EDKi):
    result = dict()
    acc = 0
    stringTemp = ""
    for i in range(0,len(EDKi)):
        stringTemp += EDKi[i]
        if(i + 1) % 6 == 0:
            result[acc] = stringTemp
            stringTemp = ""
            acc = acc + 1
    return result

#Prend un dict et renvoi un tableau en deux dimensions pour chercher une valeur plus facilement
def getMatrixFromDictio(dictio):
    x = 16
    y = 4
    matrix = {}
    for i in range(0, len(dictio)):
        tempY = 1
        if(i<16):
            tempY=1
        elif(i<32):
            tempY=2
        elif(i<48):
            tempY=3
        else:
            tempY=4
        #print( "x : " + str((i%16)+1) + " y :" +str(tempY))
        if(matrix.get(i % 16 + 1) == None):
            matrix[i % 16 + 1] = {}
        matrix[i % 16 +1][tempY] = dictio[i]
        #print("val to get : "+ str(dictio[i]))
        #print(matrix[i % 16 +1][tempY] )
    return matrix


## Applies the XOR operation
# param a, b : strings
# returns string
def exOR(a, b):
    res = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            res += "0"
        else:
            res += "1"
    return res

def rondes(G, D, keys, isInverted):
    if isInverted == 1 :
        a = 15
        b = -1
        gap = -1
    else :
        a = 0
        b = 16
        gap = 1
    for i in range(a,b,gap):
        ED = permute(D,E) # expansion
        EDKi = exOR(ED, keys[i]) # XOR
        blocks = get8BlocsOf6Bits(EDKi) # 8 blocs
        newD = ""
        for j in range(0,8):
            n = int(str(blocks[j][0]) + str(blocks[j][5]), 2)
            m = int(str(blocks[j][1]) + str(blocks[j][2]) + str(blocks[j][3]) + str(blocks[j][4]), 2)
            blocks[j] = '{0:04b}'.format(S[j][n][m])
            newD = newD + str(blocks[j])
        newG = D
        newD = exOR(permute(newD,P), G)
        D = newD
        G = newG
    return G+D



#########################################
#                                       #
#                D E S                  #
#                                       #
#########################################
def des(keys, inputFile, outputFile):
    encodedMessage = ""
    for bloc in fractionText(inputFile): # Fractionnement du texte en blocs de 64 bits (8 octets)
        bloc = permute(bloc, PI) # Permutation initiale
        G = getLeft(bloc)
        D = getRight(bloc)
        GD = rondes(G, D, keys, 0)
        encodedMessage += dictToString(permute(GD, PII))

    writeFile(encodedMessage, outputFile)

## Encodes a message using DES algorithm
# keyName : string - the name of the file containing the key
# originalMessage : string - the name of the file containing the original message
# encodedMessage : string - the name of the file where the encoded message will be written
def encode_des(keyName, originalMessage, encodedMessage):
    key = openKey(keyName)
    if key == -1 : return 0

    keys = get16KeysFromKey(key)
    des(keys, originalMessage, encodedMessage)


## Decodes a message that was encoded with the DES algorithm
# keyName : string - the name of the file containing the key
# message : string - the name of the file containing the encoded message
# decodedMessage : string - the name of the file where the decoded message will be written
def decode_des(keyName, message, decodedMessage):
    key = openKey(keyName)
    if key == -1 : return 0

#     keys = reverseKeys(get16KeysFromKey(key))
#     des(keys, "encoded_message.txt", "decoded_message.txt")
## TEST : # doing weird stuff
    keys = get16KeysFromKey(key)
    encodedMessage = ""
    for bloc in fractionText(message):
        bloc = permute(bloc, PI)
        D = getLeft(bloc)
        G = getRight(bloc)
        GD = rondes(G, D, keys, 1)
        encodedMessage += dictToString(permute(GD, PII))

    writeFile(encodedMessage, decodedMessage)


#########################################
#                                       #
#               M A I N                 #
#                                       #
#########################################
keyName = "Messages/key.txt"
originalMessage = "Messages/message.txt"
encodedMessage = "Messages/encoded_message.txt"
decodedMessage = "Messages/decoded_message.txt"

print("encode")
encode_des(keyName, originalMessage, encodedMessage)
print("decode")
decode_des(keyName, encodedMessage, decodedMessage)
