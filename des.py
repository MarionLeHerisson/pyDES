from constants import *
from resources import *


def getLeft(bloc):
    G = dict()

    for i in range((len(bloc)//2)): #on est sur 56 et non 64, il faut couper en 28
        G[i] = bloc[i]

    return G


def getRight(bloc):
    D = dict()

    for i in range((len(bloc)//2), len(bloc)):
        D[i - (len(bloc)//2)] = bloc[i]

    return D


# bloc and matrix are dictionaries
def permute(bloc, matrix):
    newbloc = dict()
    for i in range(len(bloc)-8): #TODO alors, il faut mettre -8, mais je ne sais pas du tout pk, les espaces?
        newbloc[i] = bloc[matrix[i] - 1]
    return newbloc


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


def dictToString(dict):
    acc = ""
    for i in range(0, len(dict)):
        acc += dict[i]

    return acc


def get16KeysFromKey(key):
    keys = dict()
    # separer la clé en deux
    tempG = dictToString(getLeft(key))
    tempD = dictToString(getRight(key))
    for i in range(0, 16):
        # shift G
        tempG = shiftKeyBy8(tempG)
        # shift D
        tempD = shiftKeyBy8(tempD)
        # concatener G et D
        tempGD = tempG + tempD
        # permuter GD par CP2
        key = permute(tempGD, CP2)
        print("Permuted k"+str(i+1)+" :"+dictToString(key))

        keys[i] = key
    return keys


def getKeyFromFileName(fileName):
    f = open(fileName, "r")
    content = f.read()
    if content != "" or len(content) != 64:
        return content
    else:
        return ""


def exOR(matrix, key):
    return 0


def openKey(inputFile):
    try:
        f = open(inputFile, "r")
        content = f.read()
        f.close()

        try:
            if len(content) == 64:
                return content

        except:
            print(" Error : invalid key")
            return -1

    except:
        print(" Error : file " + inputFile + " not found")
        return -1

def ronde():
    return 0


#########################################
#                                       #
#                D E S                  #
#                                       #
#########################################
def encode_des():
    # TODO il faut faire une boucle de 1 à 6 ici non ? et mettre genre "fileName"="/Messages/Clef_de_1.txt"
    # TODO et la key = fileName += i
    # TODO : entrer clé & fichier en ligne de commande

    i = 1
    inputFile = "M.txt"
    keyFileName = "testKey.txt"

    K = dict()
    blocs = []

    # au choix :shrug:
    key = getKeyFromFileName("/Messages/Clef_de_" + str(i) + ".txt")
    key = openKey(keyFileName)
    if key == -1: return 0

    print64(key)
    K = convert64to56(key)
    print56(K)

    # permutation initial
    K = permute(K, CP1)  # TODO TO BE CONTINUED -> ERROR INDEX OUT OF RANGE
    # print56(K)

    # La permutation initial par CP1 est faite, on permute 16 fois par CP2
    keys = get16KeysFromKey(K)

    # Fractionnement du texte en blocs de 64 bits (8 octets)
    for bloc in fractionText(inputFile):
        # Permutation initiale des blocs
        bloc = permute(bloc, PI)
        # Découpage des blocs en deux parties: gauche et droite, nommées G et D ;
        G = getLeft(bloc)
        D = getRight(bloc)

        #   Etapes de permutation et de substitution répétées 16 fois (appelées rondes) ;
        for i in range(16):
            D = permute(D, E)  # Expansion de D0
            printBloc(D)


#         D = exOR(D, K) # OU exclusif avec la clé K1   # TODO
#         printBloc(D)
#   Recollement des parties gauche et droite puis permutation initiale inverse.

# print64(key)
# K = convert64to56(key)
# print56(key)


#########################################
#                                       #
#               M A I N                 #
#                                       #
#########################################

# encode_des()
get16KeysFromKey("11000000000111110100100011110010111101001001011010111111")
