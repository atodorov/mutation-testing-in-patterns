def sayHello(name, title=None):
    if not title:
        title = "Mr."

    return "Hello %s %s" % (title, name)
