def sayHello(name, friends):
    if len(friends) != 0:
        raise Exception("You can't say hello to other people's friends!")

    return "Hello, " + name
