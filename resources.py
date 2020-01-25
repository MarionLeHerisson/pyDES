def printInline(element):
    if (len(str(element)) == 1):
        print(" " + str(element) + " - ", end='')
    else:
        print(str(element) + " - ", end='')


def print64(key):
    i = 0
    for bit in key:
        if (i + 1) % 8 == 0:
            print(bit)
        else:
            printInline(bit)
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
        printInline(bloc[key])
    print(" ")

def dictToString(dict):
    acc=""
    for i in range(0,len(dict)):
        acc = acc + dict[i]
    return acc
