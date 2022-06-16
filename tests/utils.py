import prtpy


def functions_in_class(theclass):
    for funcname in dir(theclass):
        print(funcname)
        if funcname.startswith('__'):
            continue
        yield getattr(theclass, funcname)

if __name__ == '__main__':

    [i for i in functions_in_class(prtpy.partitioning)]