from utils.Scraper.Base import Scraper
from bs4 import BeautifulSoup
import time
from utils.UrlUtils import UrlUtils

class ScraperScroll(Scraper):
  def afterFetchHtml(self, driver):
    domain = self.options["domain"]
    fileName = UrlUtils.onlyAzAndDigit(domain)

    driver.save_screenshot('{0}-0.png'.format(fileName))
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    time.sleep(1)

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.save_screenshot('{0}-1.png'.format(fileName))

    return
  
  def parseHtml(self, html):
    bs = BeautifulSoup(html, 'html.parser')
    return bs.find_all('a')