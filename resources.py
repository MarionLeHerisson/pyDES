def printInline2(element):
    if (len(str(element)) == 1):
        print(" " + str(element) + " - ", end='')
    else:
        print(str(element) + " - ", end='')


## Prints a string in two dimensions
# param key : string of 64 characters
def print64(key):
    i = 0
    for bit in key:
        if (i + 1) % 8 == 0:
            print(bit)
        else:
            print(bit, end = '')
        i += 1
    print(" ")


def print56(key):
    i = 0
    for bit in key:
        if (i + 1) % 7 == 0:
            print(bit)
        else:
            printInline(bit)
        i += 1
    print(" ")


def printBloc(bloc):
    for key in bloc:
        print(bloc[key], end = '')
    print(" ")

def dictToString(dict):
    acc=""
    for i in range(0,len(dict)):
        acc = acc + dict[i]
    return acc


def getValueXY(dico, x, y):
    matrix = getMatrixFromDictio(dico)
    return matrix[x][y]

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

def getKeyFromFileName(fileName):
    f = open(fileName, "r")
    content = f.read()
    if content != "" or len(content) != 64:
        return content
    else:
        return ""

def writeEncodedMessage(message):
    f = open("encoded_message.txt", "a")
    f.write(message)
    f.close()
