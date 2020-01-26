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

    print(math.ceil(len(content)/64))

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
    i = 0
#     if isInverted == 1 :
#         a = 15
#         b = -1
#         gap = -1
#     else :
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
#         print("RONDE "+str(i+1))
#         print("G = "+G)
#         print("D = "+D)
#         print(" ")
#     return bin_to_str(G)+bin_to_str(D)
    return G+D



#########################################
#                                       #
#                D E S                  #
#                                       #
#########################################
def des(keys, inputFile, outputFile):
    encodedMessage = ""
    for bloc in fractionText(inputFile): # Fractionnement du texte en blocs de 64 bits (8 octets)
        printBloc(bloc)
        bloc = permute(bloc, PI) # Permutation initiale
        G = getLeft(bloc)
        D = getRight(bloc)
        GD = rondes(G, D, keys, 0)
        encodedMessage += dictToString(permute(GD, PII))

    writeFile(encodedMessage, outputFile)

def encode_des():
#     key = getKeyFromFileName("/Messages/Clef_de_"+str(i)+".txt")
    key = openKey("testKey.txt")
    if key == -1 : return 0

    keys = get16KeysFromKey(key)
    des(keys, "M.txt", "encoded_message.txt")


def decode_des():
    key = openKey("testKey.txt")
    if key == -1 : return 0

    keys = reverseKeys(get16KeysFromKey(key))
    des(keys, "encoded_message.txt", "decoded_message.txt")



#########################################
#                                       #
#               M A I N                 #
#                                       #
#########################################

print("encode")
encode_des()
print("decode")
decode_des()

print(bin2txt("10001111100101110010111010111110011"))

## TESTS ##

# get16KeysFromKey("11000000000111110100100011110010111101001001011010111111")
# lesBlocs = get8BlocsOf6Bits("110001100111111100101010010101111000111101001101")
# print(lesBlocs)
#print(rondes("01111101101010110011110100101010", "01111111101100100000001111110010", get16KeysFromKey("11000000000111110100100011110010111101001001011010111111")))

# rondes("01111101101010110011110100101010", "01111111101100100000001111110010", get16KeysFromKey("11000000000111110100100011110010111101001001011010111111"))



# M =  1101110010111011110001001101010111100110111101111100001000110010100111010010101101101011111000110011101011011111
# M2 = 11011100101110111100010011010101111001101111011111000010001100101001110100101011011010111110001100111010110111110000000000000000
