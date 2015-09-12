import PyDictionary

def find_syns(word):
    dict = PyDictionary.PyDictionary()
    return {'syns': dict.synonym(word)}