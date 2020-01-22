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

# bloc and matrix are dictionaries
def permute(bloc, matrix):
  newbloc = dict()

  for i in range(len(bloc)):
    newbloc[i] = bloc[matrix[i] - 1]

  return newbloc

def fractionText(inputFile):
  f = open(inputFile, "r")
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

def exOR(matrix, key):
  return 0

def openKey(inputFile):
  try :
    f = open(inputFile, "r")
    content = f.read()
    f.close()

    try:
      if len(content) == 64:
        return content

    except :
      print(" Error : invalid key")
      return -1

  except:
      print(" Error : file " + inputFile + " not found")
      return -1

#########################################
#                                       #
#                D E S                  #
#                                       #
#########################################
def encode_des():
  # TODO : entrer clé & fichier en ligne de commande
  inputFile = "M.txt"
  keyFileName = "testKey.txt"

  K = dict()
  blocs = []

  key = openKey(keyFileName)
  if key == -1 : return 0

  print64(key)
  K = convert64to56(key)
  print56(K)

  K = permute(K, CP1)   # TODO TO BE CONTINUED -> ERROR INDEX OUT OF RANGE
  print56(K)

  # Fractionnement du texte en blocs de 64 bits (8 octets)
  for bloc in fractionText(inputFile):
    # Permutation initiale des blocs
    bloc = permute(bloc, PI)
    # Découpage des blocs en deux parties: gauche et droite, nommées G et D ;
    G = getLeft(bloc)
    D = getRight(bloc)

    #   Etapes de permutation et de substitution répétées 16 fois (appelées rondes) ;
    for i in range (16):
        D = permute(D, E) # Expansion de D0
        printBloc(D)
#         D = exOR(D, K) # OU exclusif avec la clé K1   # TODO
#         printBloc(D)
  #   Recollement des parties gauche et droite puis permutation initiale inverse.



#########################################
#                                       #
#               M A I N                 #
#                                       #
#########################################

encode_des()