from constants import *
from resources import *

def getLeft(bloc):
  G = dict()

  for i in range(32):
    G[i] = bloc[i]

  return G

def getRight(bloc):
  D = dict()

  for i in range(32, 64):
    D[i - 32] = bloc[i]

  return D

def permute(bloc, matrix):
  newbloc = dict()

  for i in range(len(bloc)):
    newbloc[i] = bloc[matrix[i] - 1]

  return newbloc

def fractionText(inputFile):
  f = open("M.txt", "r")
  content = f.read()
  cursor = 0
  bloc = dict()
  loop = 1

  while loop :
    for i in range(0, 64):
      try :
        bloc[i] = content[cursor]
        cursor += 1
      except :
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

def shiftKey(key):
  newKey=""
  for i in range(0,16):
    newKey += key[(i+1)%16]
  return newKey

def get16KeysFromKey(key):
  keys = dict(16)
  for i in range(0, 16):
    key = shiftKey(key)
    keys[i] = key
  return keys

def getKeyFromFileName(fileName):
  f = open(fileName, "r")
  content = f.read()
  if content != "" or len(content)!=64:
    return content
  else:
    return ""



#########################################
#                                       #
#                D E S                  #
#                                       #
#########################################
def encode_des():
  #TODO il faut faire une boucle de 1 à 6 ici non ? et mettre gnre "fileName"="/Messages/Clef_de_1.txt"
  #TODO et la key = fileName += i
  #key = "0100110010101110110111001010110111000100011010001100100000101010"
  key = getKeyFromFileName("/Messages/Clef_de_1.txt")
  inputFile = "M.txt"
  K = dict()
  blocs = []

  # Fractionnement du texte en blocs de 64 bits (8 octets)
  for bloc in fractionText(inputFile):
    # Permutation initiale des blocs
    bloc = permute(bloc, PI)
    # Découpage des blocs en deux parties: gauche et droite, nommées G et D ;
    G = getLeft(bloc)
    D = getRight(bloc)

    #   Etapes de permutation et de substitution répétées 16 fois (appelées rondes) ;
    for i in range (16):
        D = permute(D, E)
        printBloc(D)
  #   Recollement des parties gauche et droite puis permutation initiale inverse.

  # TODO : key = open & read file key
  # TODO : verif que la clé fait bien 64 bits

  # print64(key)
  # K = convert64to56(key)
  # print56(key)

  #keys=get16KeysFromKey(K)



#########################################
#                                       #
#               M A I N                 #
#                                       #
#########################################

encode_des()