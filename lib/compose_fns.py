def compose_fns(*fns):
    return lambda: [fn() for fn in fns if fn]
