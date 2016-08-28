def xnor_raise(list_a, list_b):
    valid_lists = 0
    if list_a:
        valid_lists += 1

    if list_b:
        valid_lists += 1

    if valid_lists != 1:
        raise Exception('TEST')
