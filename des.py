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

#########################################
#                                       #
#                D E S                  #
#                                       #
#########################################
def encode_des():
  key = "0100110010101110110111001010110111000100011010001100100000101010"
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



#########################################
#                                       #
#               M A I N                 #
#                                       #
#########################################

encode_des()