from constants import *
from resources import *

## Gets 32 first bits of a 64 bits matrix
# param bloc : size 64 dictionary
# returns size 32 dictionary
def getLeft(bloc):
  G = dict()

  for i in range(32):
    G[i] = bloc[i]

  return G

## Gets 32 last bits of a 64 bits matrix
# param bloc : size 64 dictionary
# returns size 32 dictionary
def getRight(bloc):
  D = dict()

  for i in range(32, 64):
    D[i - 32] = bloc[i]

  return D

## permutes bits of a bloc in accordance to the given matrix
# param bloc : size N dictionary
# param matrix : size N dictionary
# returns size N dictionary
def permute(bloc, matrix):
  newbloc = dict()

  for i in range(len(bloc)):
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

## Gets a key from a file name
# pram inputFile : string "example.txt"
# returns string | int
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
  # TODO il faut faire une boucle de 1 à 6 ici non ? et mettre genre "fileName"="/Messages/Clef_de_1.txt"
  # TODO et la key = fileName += i
  # OU BIEN
  # TODO : entrer clé & fichier en ligne de commande

  i=1
  inputFile = "M.txt"
  keyFileName = "testKey.txt"

  K = dict()
  blocs = []

  # au choix :shrug:
  key = getKeyFromFileName("/Messages/Clef_de_"+str(i)+".txt")
  key = openKey(keyFileName)
  if key == -1 : return 0

##### GENERATION DES CLES #####
  print64(key)
  K = convert64to56(key)
  print56(K)

  K = permute(K, CP1)   # TODO TO BE CONTINUED -> ERROR INDEX OUT OF RANGE
  print56(K)

##### CHIFFREMENT DES #####
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
        D = exOR(D, K) # OU exclusif avec la clé K1
  #   Recollement des parties gauche et droite puis permutation initiale inverse.

  #keys=get16KeysFromKey(K)




#########################################
#                                       #
#               M A I N                 #
#                                       #
#########################################

encode_des()