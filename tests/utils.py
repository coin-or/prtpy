def functions_in_class(theclass):
    for funcname in dir(theclass):
        if funcname.startswith('__'):
            continue
        yield getattr(theclass, funcname)
