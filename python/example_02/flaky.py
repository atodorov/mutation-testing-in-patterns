def log_to_file(content):
  data_file = open('./test.txt', 'a+')
  data_file.write(content)
  data_file.close()

def sayHello(times=2, upcase = False):
    text = 'Hello World\n'

    if upcase:
        text = text.upper()

    for i in range(times):
        log_to_file(text)
