from GoodreadsGraph import GoodReadsGraph
from WebScraper import WebScraper
from GestionPickle import GestionPickle

url = 'https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once'
scrap = WebScraper.scraper(url)
GestionPickle.guardarPickle( scrap, 'listaObjetos2.0')   

eo = GoodReadsGraph()
eo.CreateGraph()
eo.CreateRelation()
eo.fillGraph()

#primera consulta
eo.ListaLibrosAutor()

'''
#segunda consulta
eo.LibrosDelMismoGeneroYdecada()

#tercera consulta
eo.listaAutoresGeneroX()

#cuarta consulta
eo.RecomendarLibrosPuntajeGenero()

#quinta consulta
eo.librosPorXplata()

'''