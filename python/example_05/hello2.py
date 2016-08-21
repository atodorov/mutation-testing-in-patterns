def sayHello(name, friends):
    if friends:
        raise Exception("You can't say hello to other people's friends!")

    return "Hello, " + name
