import pickle

class GestionPickle:

    def guardarPickle(lista, nombre_archivo):
        with open(nombre_archivo, 'wb') as archivo:
            pickle.dump(lista, archivo)

    def cargarPickle(nombre_archivo):
        with open(nombre_archivo, 'rb') as archivo:
            return pickle.load(archivo)
    