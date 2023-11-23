from Graph import Grafo
from GestionPickle import GestionPickle
from Relations import Relation
import inquirer

class GoodReadsGraph:

    def __init__(self):
        self.graph = None
        self.relations = None

    def getGraph(self): return self.graph

    def setGraph(self, newGraph): self.graph = newGraph

    def getRealation(self): return self.relations

    def setRelation(self, newList): self.relations = newList

    def CreateGraph(self):
        grafo = Grafo()
        self.setGraph(grafo)
    
    def CreateRelation(self):
        first  = Relation('escrito_por', 1)
        second = Relation('publicado_el', 2)
        third = Relation('vendidoPorPrecio_de', 3)
        fourth = Relation('calificacion_de', 4)
        fifth = Relation('libroConGeneros_de', 5)
        sixth = Relation('escribio_a', 6)
        seven = Relation('autorEscribioGenero_de',7)
        eight = Relation('GeneroPresente_en',8)
        self.setRelation([first, second, third, fourth, fifth, sixth, seven, eight])

    def fillGraph(self):
        listaObjetos = GestionPickle.cargarPickle('listaObjetos2.0')       
        for i in range(len(listaObjetos)):
            objetotitulo = None
            objetoAutor = None
            for j in range(len(listaObjetos[i])):
                verificacion = self.getGraph().verificarListaNodos(listaObjetos[i][j])
                if type(listaObjetos[i][j]).__name__ == 'Title':
                    objetotitulo = listaObjetos[i][j]
                elif type(listaObjetos[i][j]).__name__ == 'AutorName':
                    objetoAutor = verificacion
                    self.getGraph().adArista(objetotitulo, verificacion,1)
                    self.getGraph().adArista(verificacion, objetotitulo,6)
                elif type(listaObjetos[i][j]).__name__ == 'tuple':
                    day, month, year = listaObjetos[i][j]
                    self.getGraph().adArista(objetotitulo, self.getGraph().verificarListaNodos(day),2)
                    self.getGraph().adArista(objetotitulo, self.getGraph().verificarListaNodos(month),2)
                    self.getGraph().adArista(objetotitulo, self.getGraph().verificarListaNodos(year),2)
                elif type(listaObjetos[i][j]).__name__ == 'Price':
                    self.getGraph().adArista(objetotitulo, verificacion,3)
                elif type(listaObjetos[i][j]).__name__ == 'Score':
                    self.getGraph().adArista(objetotitulo, verificacion,4)
                elif type(listaObjetos[i][j]).__name__ == 'list':
                    for eo in listaObjetos[i][j]:
                        self.getGraph().adArista(objetotitulo, self.getGraph().verificarListaNodos(eo),5)
                        self.getGraph().adArista(objetoAutor, self.getGraph().verificarListaNodos(eo),7)
                        self.getGraph().adArista(self.getGraph().verificarListaNodos(eo), objetotitulo, 8)


#primera consulta----------------------
    def ListaLibrosAutor(self):
        autores = self.listaObjetosAutor()
        autoresenCadena = [str(autor) for autor in autores]
        ListaOpciones = [inquirer.List('Opcion',
                                      message='elige una opcion',
                                      choices=autoresenCadena)]
        
        dicRespuesta = inquirer.prompt(ListaOpciones)
        respuesta = autores[autoresenCadena.index(dicRespuesta['Opcion'])]

        listaPosicionesLibros = [posicion for posicion, valor in enumerate(self.getGraph().matrix[self.getGraph().nodos.index(respuesta)]) if valor == 6]

        listaFechas = []
        for fila in listaPosicionesLibros:
            nuevaFecha = [None,None,None]
            for columna in range(len(self.getGraph().matrix[fila])):
                if self.getGraph().matrix[fila][columna] == 2: 
                    if type(self.getGraph().nodos[columna]).__name__ == 'ReleaseDay':
                        nuevaFecha[0] = self.getGraph().nodos[columna].value
                    elif type(self.getGraph().nodos[columna]).__name__ == 'ReleaseMont':
                        nuevaFecha[1] = self.getGraph().nodos[columna].value
                    elif type(self.getGraph().nodos[columna]).__name__ == 'ReleaseYear':
                        nuevaFecha[2] = self.getGraph().nodos[columna].value
            
            listaFechas.append(nuevaFecha)

        listaLibros = [self.getGraph().nodos[posicion].value for posicion in listaPosicionesLibros]
        union = list(zip(listaLibros, listaFechas))
        libros_ordenados = sorted(union, key=lambda libro: (libro[1][2], libro[1][1], libro[1][0]), reverse=True)
        for libro in libros_ordenados:
            print(libro)

#segunda consulta----------------------------
    def LibrosDelMismoGeneroYdecada(self):
        libros = self.listaObjetosLibro()
        librosenCadena = [str(titulo) for titulo in libros]
        ListaOpciones = [inquirer.List('Opcion',
                                      message='elige un libro',
                                      choices=librosenCadena)]

        dicRespuesta = inquirer.prompt(ListaOpciones)
        Librorespuesta = libros[librosenCadena.index(dicRespuesta['Opcion'])]
        
        numero = int(input('Escribe el numero de libro que quieres que te recomiende en base al libro seleccionado: '))

        posicionesLibros = [self.getGraph().nodos.index(libro) for libro in libros]

        listainfolibros = self.listaLibroYearGeneros(posicionesLibros)

        infolibroRespuesta = None
        romperBucle = False

        for lista in listainfolibros:
            if romperBucle == True:
                break
            for posicion in lista:
                if posicion == Librorespuesta:
                    infolibroRespuesta = lista
                    romperBucle = True
                    break

        librosFinal = [posicion for posicion in listainfolibros if
                    posicion[0] != infolibroRespuesta[0] and
                    (str(posicion[1])[0]+ str(posicion[1])[1] + str(posicion[1])[2]) == (str(infolibroRespuesta[1])[0]+ str(infolibroRespuesta[1])[1] + str(infolibroRespuesta[1])[2]) and
                    any(genero in posicion[2] for genero in infolibroRespuesta[2])]

        print(f'el libro escogido fue: \n{infolibroRespuesta}\n')

        if numero > len(librosFinal):
            print('aunque el numero que pusiste supera a los libros que estan te recomendaremos los que tenemos')
        else:
            librosFinal = librosFinal[:numero]
        
        print('las recomendaciones son:')
        for posicion in librosFinal:
            print(posicion)

#tercera consulta--------------------------
    def listaAutoresGeneroX(self):
        generos = self.listaObjetosGenero()
        generosenCadena = [str(genero) for genero in generos]
        ListaOpciones = [inquirer.List('Opcion',
                                      message='elige un genero',
                                      choices=generos)]

        dicRespuesta = inquirer.prompt(ListaOpciones)
        Generorespuesta = generos[generosenCadena.index(dicRespuesta['Opcion'])]

        posicionGeneroRespuesta = self.getGraph().nodos.index(Generorespuesta)

        libros = self.listaObjetosLibro()
        librosEseGenero = [posicion for posicion in libros if self.getGraph().matrix[self.getGraph().nodos.index(posicion)][posicionGeneroRespuesta] == 5]
        autores = self.listaObjetosAutor()
        autoreEseGenero = [posicion for posicion in autores if self.getGraph().matrix[self.getGraph().nodos.index(posicion)][posicionGeneroRespuesta] == 7]

        listaAutoresLibrosXgeneroRespuesta = []

        for autor in autoreEseGenero:
            infoAutor = [autor, 0]
            for libro in librosEseGenero:
                if self.getGraph().matrix[self.getGraph().nodos.index(autor)][self.getGraph().nodos.index(libro)] == 6:
                    infoAutor[1] += 1
            listaAutoresLibrosXgeneroRespuesta.append(infoAutor)

        listaOrdenada = sorted(listaAutoresLibrosXgeneroRespuesta, key=lambda x: x[1], reverse=True)

        print(f'estos son los autores que mas libros han escrito del genero {Generorespuesta}')
        for lista in listaOrdenada:
            print(lista)
    #Cuarta consulta--------------
    def RecomendarLibrosPuntajeGenero(self):
        
        Generorespuesta = self.menuGeneros()
        puntaje = int(input('Escribe de 1 a 5 el puntaje que quieres los libros: '))

        listainfoLibro = self.listaLibrosGeneros()

        listafinal = []

        for posicion in listainfoLibro:
            if posicion[1] >= puntaje and all(elemento in posicion[2] for elemento in Generorespuesta) == True:
                listafinal.append(posicion)

        print(f'Los libros de los generos: \n{Generorespuesta} \n\nque tienen un puntaje mayor o igual a {puntaje} son:\n')

        for posicion in listafinal:
            print(posicion)

    #quinta consulta--------------------------------------
    def librosPorXplata(self):
        Generorespuesta = self.menuGeneros()

        listainfoLibro = self.listaLibrosGenerosPlata([posicion for posicion in self.getGraph().nodos if type(posicion).__name__ == 'Title'])

        listafinal = []

        for posicion in listainfoLibro:
            if any(elemento in posicion[2] for elemento in Generorespuesta) == True:
                listafinal.append(posicion)

        presupuesto = int(input('ingrese el presupuesto que tiene para comprar: '))
        
        listaRespuesta = self.funcionRecursiva(listafinal, presupuesto)
        listaRespuestCompleta = self.listaLibrosGenerosPrecio(listaRespuesta)
        for posicion in listaRespuestCompleta:
            print(posicion)

    def listaLibroYearGeneros(self, listaPoscisionesLibros):
        
        infolibros = []
        
        for libro in listaPoscisionesLibros:
            infoLibro = [self.getGraph().nodos[libro], None, []]
            for posicion in range(len(self.getGraph().matrix[libro])):
                if self.getGraph().matrix[libro][posicion] == 2 and type(self.getGraph().nodos[posicion]).__name__ == 'ReleaseYear':
                    infoLibro[1] = self.getGraph().nodos[posicion]
                elif self.getGraph().matrix[libro][posicion] == 5:
                    infoLibro[2].append(self.getGraph().nodos[posicion])
            infolibros.append(infoLibro)
        
        return infolibros

    def menuGeneros(self):
        generos = [posicion for posicion in self.getGraph().nodos if type(posicion).__name__ == 'Genres']
        generosenCadena = [str(genero) for genero in generos]
        
        ListaOpciones = [inquirer.Checkbox('Opciones',
                                        message='Elige un género',
                                        choices=generos)]
        dicRespuesta = inquirer.prompt(ListaOpciones)
        opciones_seleccionadas = dicRespuesta['Opciones']
        
        Generorespuesta = [generos[generosenCadena.index(posicion)] for posicion in opciones_seleccionadas]
        return Generorespuesta

    def LibrosGeneros(self):
        infolibros = []
        libros = self.listaObjetosLibro()
        
        for libro in libros:
            posicionLibro = self.getGraph().nodos.index(libro)
            infoLibro = [self.getGraph().nodos[posicionLibro], None, []]
            for posicion in range(len(self.getGraph().matrix[posicionLibro])):
                if self.getGraph().matrix[posicionLibro][posicion] == 4:
                    infoLibro[1] = self.getGraph().nodos[posicion].value
                elif self.getGraph().matrix[posicionLibro][posicion] == 5:
                    infoLibro[2].append(self.getGraph().nodos[posicion])
            infolibros.append(infoLibro)

        return infolibros
    
    def maximisarCompra(self, lista_libros, presupuesto, actual = 0, seleccionados = None):
        if seleccionados is None:
            seleccionados = []

        if actual == len(lista_libros):
            return seleccionados

        nombre_libro, precio, _ = lista_libros[actual]

        if precio <= presupuesto:
            seleccion_con_actual = self.maximisarCompra(lista_libros, presupuesto - precio, actual + 1, seleccionados + [nombre_libro])
        else:
            seleccion_con_actual = []

        seleccion_sin_actual = self.maximisarCompra(lista_libros, presupuesto, actual + 1, seleccionados)

        return seleccion_con_actual if len(seleccion_con_actual) > len(seleccion_sin_actual) else seleccion_sin_actual

    def listaLibrosGenerosPrecio(self, libros):
        infolibros = []
        
        for libro in libros:
            posicionLibro = self.getGraph().nodos.index(libro)
            infoLibro = [self.getGraph().nodos[posicionLibro], None, []]
            for posicion in range(len(self.getGraph().matrix[posicionLibro])):
                if self.getGraph().matrix[posicionLibro][posicion] == 3:
                    infoLibro[1] = self.getGraph().nodos[posicion].value
                elif self.getGraph().matrix[posicionLibro][posicion] == 5:
                    infoLibro[2].append(self.getGraph().nodos[posicion])
            infolibros.append(infoLibro)

        return infolibros
    
    def listaObjetosLibro(self):
        return [posicion for posicion in self.getGraph().nodos if type(posicion).__name__ == 'Title']
    
    def listaObjetosGenero(self):
        return [posicion for posicion in self.getGraph().nodos if type(posicion).__name__ == 'Genres']

    def listaObjetosAutor(self):
        return [posicion for posicion in self.getGraph().nodos if type(posicion).__name__ == 'AutorName']

        

                
        
        

