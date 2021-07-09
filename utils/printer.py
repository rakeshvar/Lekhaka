
def slab_print_255(slab, col_names=None):
    """
    Prints a 'slab' of printed 'text' using ascii.
    :param slab: A matrix of floats from [0, 1]
    """
    for ir, r in enumerate(slab/255.):
        print('{:2d}¦'.format(ir), end='')
        for val in r:
            if   val < 0.0:     print('-', end='')
            elif val < .15:     print(' ', end=''),
            elif val < .35:     print('░', end=''),
            elif val < .65:     print('▒', end=''),
            elif val < .85:     print('▓', end=''),
            elif val <= 1.:     print('█', end=''),
            else:               print('+', end='')
        print('¦ {}'.format(col_names[ir] if col_names else ''))

