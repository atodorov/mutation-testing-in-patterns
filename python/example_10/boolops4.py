def xnor_raise(list_a, list_b):
    if not any([list_a, list_b]) or all([list_a, list_b]):
        raise Exception('TEST')
