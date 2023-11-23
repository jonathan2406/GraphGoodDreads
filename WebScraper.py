import pickle
from urllib.request import urlopen
from bs4 import BeautifulSoup
from AutorName import AutorName
from Genres import Genres
from Price import Price
from Score import Score
from Title import Title
from releaseDay import ReleaseDay
from releaseMont import ReleaseMont
from releaseYear import ReleaseYear
from GestionPickle import GestionPickle

class WebScraper:

  def load_content(url):
    content = urlopen(url) 
    bs = BeautifulSoup(content.read()) 
    return bs 

  def scrape_title(book_url_content):
    bookTitle = book_url_content.find("h1",{"data-testid":"bookTitle"}).get_text()
    return Title(bookTitle.strip())

  def scrape_autorName(book_url_content):
    bookAutorName = book_url_content.find("span",{"data-testid":"name"}).get_text()
    return AutorName(bookAutorName.strip())

  def scrape_realese(book_url_content):
    bookRelease = book_url_content.find("p",{"data-testid":"publicationInfo"}).get_text()
    bookRelease = bookRelease.strip()
    aux = bookRelease.replace(',','')
    meses = {'January':1, 'February':2, 'March':3, 'April':4, 'May':5, 'June':6, 'July':7, 'August':8, 'September':9, 'October':10, 'November':11, 'December':12}
    aux = aux.split(' ')
    for i in range(len(aux)):
        if aux[i] not in meses and aux[i].isdigit() == False:
          aux[i] = None
        elif aux[i] in meses:
          aux[i] = meses[aux[i]]
        else:
          aux[i] = int(aux[i])
    while(None in aux):
      aux.pop(aux.index(None))
    retorno = (ReleaseDay(aux[1]), ReleaseMont(aux[0]), ReleaseYear(aux[2]))
    
    return retorno

  def scrape_price(book_url_content):
    bookScore = str(book_url_content.findAll("div",{"class":"BookActions"}))
    string = ''
    for i in range(len(bookScore)):
      if bookScore[i] == '$':
        string += bookScore[i+1] + bookScore[i+2] + bookScore[i+3] + bookScore[i+4]
        if bookScore[i+5].isdigit() == True:
          string += bookScore[i+5]
        aux = string.strip()
        return Price(float(aux))
      
    if len(string) == 0:
      return Price(0)

  def scrape_score(book_url_content):
    bookScore = book_url_content.find("div",{"class":"RatingStatistics__rating"}).get_text()
    aux = bookScore.strip()
    return Score(float(aux))

  def scrape_genres(book_url_content):
    bookGenres = book_url_content.findAll("span",{"class":"BookPageMetadataSection__genreButton"})
    eo = [genre.find("a",{"class":"Button Button--tag-inline Button--small"}).get_text() for genre in bookGenres]
    eo = [Genres(a) for a in eo[:3]]
    return eo

  def scrape_urls(url):
      bs_object = WebScraper.load_content(url)
      single_urls = bs_object.findAll("a",{"class":"bookTitle"})
      single_urls = [url["href"] for url in single_urls]
      base_url = "https://www.goodreads.com"
      single_urls = list(map(lambda x: base_url+x, single_urls))
      return single_urls

  def scrapeMainPage(url):
      bs_object = WebScraper.load_content(url)
      single_urls = bs_object.findAll("div",{"class":"pagination"})
      single_urls = single_urls[0].find_all('a')
      single_urls = [enlace.get('href') for enlace in single_urls[:2]]
      base_url = "https://www.goodreads.com"
      single_urls = list(map(lambda x: base_url+x, single_urls))
      single_urls.insert(0, url)
      print(single_urls)
      return single_urls

  def scraper(url):
      
      pagesToscrape = WebScraper.scrapeMainPage(url)
      single_urls = [WebScraper.scrape_urls(elemento) for elemento in pagesToscrape]
      single_urls = sum(single_urls,[])
      pageInfo = []
      for i in range(len(single_urls)):
        pageInfo.append(WebScraper.load_content(single_urls[i]))
      
      titles = list(map(WebScraper.scrape_title, pageInfo))
      autorName = list(map(WebScraper.scrape_autorName, pageInfo))
      release = list(map(WebScraper.scrape_realese, pageInfo))
      price = list(map(WebScraper.scrape_price, pageInfo))
      score = list(map(WebScraper.scrape_score, pageInfo))
      genres = list(map(WebScraper.scrape_genres, pageInfo))

      data = list(zip(titles, autorName, release, price, score, genres))
      return data
  


  





    





