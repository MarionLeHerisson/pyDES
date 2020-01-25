from constants import *
from resources import *


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
    loop = 1

    while loop:
        for i in range(0, 64):
            try:
                bloc[i] = content[cursor]
                cursor += 1
            except:
                bloc[i] = 0
                loop = 0
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


def get16KeysFromKey(key):
    keys = dict()
    tempG = dictToString(getLeft(key)) # séparer la clé en deux
    tempD = dictToString(getRight(key))
    for i in range(0, 16):
        tempG = shiftKeyBy8(tempG) # shift G
        tempD = shiftKeyBy8(tempD) # shift D
        tempGD = tempG + tempD # concatener G et D
        key = permute54(tempGD, CP2) # permuter GD par CP2
#         print("Permuted k"+str(i+1)+" :"+dictToString(key))
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


def rondes(G, D, keys):
    i = 0
    for i in range(0,16):
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
#         print("RONDE "+str(i+1))
#         print("G = "+G)
#         print("D = "+D)
#         print(" ")
    return G+D

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



#########################################
#                                       #
#                D E S                  #
#                                       #
#########################################
def encode_des():
    # TODO il faut faire une boucle de 1 à 6 ici non ? et mettre genre "fileName"="/Messages/Clef_de_1.txt"
    # TODO et la key = fileName += i
    # OU BIEN
    # TODO : entrer clé & fichier en ligne de commande

    i=1
    inputFile = "M.txt"
    keyFileName = "testKey.txt"

    K = dict()
    blocs = []
    encodedMessage = ""

#     key = getKeyFromFileName("/Messages/Clef_de_"+str(i)+".txt")
    key = openKey(keyFileName)
    if key == -1 : return 0

##### GENERATION DES CLES #####
    K = permute(key, CP1) # permutation initiale
    keys = get16KeysFromKey(K)

##### CHIFFREMENT DES #####
    # Fractionnement du texte en blocs de 64 bits (8 octets)
    for bloc in fractionText(inputFile):
        bloc = permute(bloc, PI) # Permutation initiale
        G = getLeft(bloc)
        D = getRight(bloc)
        GD = rondes(G, D, keys)
        encodedMessage += dictToString(permute(GD, PII))

    writeEncodedMessage(encodedMessage)

#########################################
#                                       #
#               M A I N                 #
#                                       #
#########################################

encode_des()

## TESTS ##
# get16KeysFromKey("11000000000111110100100011110010111101001001011010111111")
# lesBlocs = get8BlocsOf6Bits("110001100111111100101010010101111000111101001101")
# print(lesBlocs)

# rondes("01111101101010110011110100101010", "01111111101100100000001111110010", get16KeysFromKey("11000000000111110100100011110010111101001001011010111111"))
