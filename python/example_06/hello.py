def sayHello(name, title=None):
    if title is None:
        title = "Mr."

    return "Hello %s %s" % (title, name)
