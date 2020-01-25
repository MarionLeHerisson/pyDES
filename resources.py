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
