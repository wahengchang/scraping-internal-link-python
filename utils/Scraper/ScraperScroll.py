from utils.Scraper.Base import Scraper
from bs4 import BeautifulSoup
import time

class ScraperScroll(Scraper):
  def preFetchHtml(self, driver):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    time.sleep(1)
    driver.save_screenshot('{0}-0.png'.format(time.time()))

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)
    driver.save_screenshot('{0}-1.png'.format(time.time()))

    return
  
  def parseHtml(self, html):
    bs = BeautifulSoup(html, 'html.parser')
    return bs.find_all('a')