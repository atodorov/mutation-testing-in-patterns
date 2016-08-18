import myparser

def sayHello(name):
    names = myparser.parseArgs(name)

    if len(names) != 1:
        raise Exception("You can say hello to only one person at a time!")

    return "Hello, " + name
