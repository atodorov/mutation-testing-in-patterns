def xnor_raise(list_a, list_b):
    if (len(list_a) == 0 and len(list_b) == 0) or (len(list_a) > 0 and (len(list_b) > 0)):
        raise Exception('TEST')
