import requests
from utils.Scraper.Base import Scraper
from bs4 import BeautifulSoup
import time

def getFileFromUrl (url = ''):
  return url.split("/")[-1] 

class ScraperPdf(Scraper):
  def fetchHtml (self):
    domain = self.options["domain"]
    saveHtml = self.options["saveHtml"]
    _url = self.url

    if _url.endswith('.pdf'):
      url =  '{0}{1}'.format(domain, _url) if _url.startswith('/') else _url
      pathName = './{0}'.format(getFileFromUrl(url))

      print('going to download pdf file to path {0}'.format(pathName), url)
      fileContent = requests.get(url)
      f = open(pathName,'wb')
      f.write(fileContent.content)
      f.close()
        
      return ''
    else :
      return super(ScraperPdf, self).fetchHtml()

  def afterFetchHtml(self, driver):
    driver.save_screenshot('{0}-0.png'.format(time.time()))
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    time.sleep(1)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.save_screenshot('{0}-1.png'.format(time.time()))

    return
  
  def afterParseAllLinks(self, allLinks):
    t = []
    for linkString in allLinks:
      if 'journals/journalsAction/middlePeriodical?bookId=' in linkString:
        t.append(linkString)
      if linkString.endswith('.pdf'):
        t.append(linkString)

    return t