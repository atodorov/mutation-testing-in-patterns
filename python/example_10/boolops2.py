def xnor_raise(list_a, list_b):
    if (not list_a and not list_b) or (list_a and list_b):
        raise Exception('TEST')
