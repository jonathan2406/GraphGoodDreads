import time

class Grafo:
    def __init__(self):
        self.matrix = []
        self.nodos = []

    def adVertice(self, v):
        if v in self.nodos:
            return
        for filas in self.matrix:
            filas.append(-1)
        nuevaFila = []
        self.matrix.append(nuevaFila)
        for i in range(len(self.matrix)):
            nuevaFila.append(-1)
        self.nodos.append(v)

    def adArista(self, v1, v2, relacion):

        verificacionv1 = self.verificarListaNodos(v1)
        if verificacionv1 == v1:
            self.adVertice(v1)
 
        verificacionv2 = self.verificarListaNodos(v2)
        if verificacionv2 == v2:
            self.adVertice(v2)

        posicionV1 = self.nodos.index(verificacionv1)
        posicionV2 = self.nodos.index(verificacionv2)

        self.matrix[posicionV1][posicionV2] = relacion

    def verificarListaNodos(self, nodo):
        for posicion in range(len(self.nodos)):
            if type(self.nodos[posicion]) == type(nodo) and nodo.value == self.nodos[posicion].value:
                return self.nodos[posicion]
        return nodo
    
    def printMatriz(self):
        for filas in self.matrix:
            print(filas)

    def GradoEntrante(self,v):
        if v not in self.nodos:
            print("grave")
            return
        cont = 0
        posicionV = self.nodos.index(v)
        for filas in self.matrix:
            if filas[posicionV] == 1:
                cont += 1
        print(f"el grado entrante del nodo {v} es {cont}")

    def GradoSaliente(self, v):
        if v not in self.nodos:
            print("grave")
            return
        cont = 0
        posicionV = self.nodos.index(v)
        for i in range(len(self.matrix[posicionV])):
            if self.matrix[posicionV][i] == 1:
                cont += 1
        print(f"el grado saliente del nodo {v} es {cont}")

    def eliminarVertice(self, v):
        if v not in self.nodos:
            print("grave")
            return
        posicionV = self.nodos.index(v)
        self.matrix.pop(posicionV)
        for filas in self.matrix:
            filas.pop(posicionV)

        self.nodos.remove

    def calcularRutas(self, puntoA, puntoB, visitados=set(), ruta=[], rutas=[]):
        if puntoA in visitados:
            return rutas
        visitados.add(puntoA)
        for i in range(len(self.nodos)):
            if self.matrix[self.nodos.index(puntoA)][i] >= 0:
                if self.nodos[i] not in ruta:
                    nueva_ruta = ruta.copy()
                    nueva_ruta.append(self.matrix[self.nodos.index(puntoA)][i])

                    if self.nodos[i] == puntoB:
                        rutas.append(nueva_ruta)
                    else:
                        rutas = self.calcularRutas(self.nodos[i], puntoB, visitados, nueva_ruta, rutas)
        visitados.remove(puntoA)
        return rutas


