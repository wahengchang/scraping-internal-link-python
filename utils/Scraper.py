import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from utils.FileHelper import FileHelper
from utils.UrlUtils import UrlUtils

driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME)

def joinList(arr1 = [], arr2 = []):
  return list(set( arr1 + arr2 ))

class Scraper:
  def __init__(self, url, innerLinks, gtpLinks):
    self.url = url
    self.allLinks = []
    self.innerLinks = innerLinks
    self.gtpLinks = gtpLinks
    self.newInnerLinks = []
    self.newgtpLinks = []

  def parseHtml(self, html):
    bs = BeautifulSoup(html, 'html.parser')
    return bs.find_all('a')

  # @staticmethod
  def processLinks(self):
    url         = self.url
    innerLinks = self.innerLinks
    gtpLinks = self.gtpLinks

    driver.get(url)
    print('[INFO] processing %s' % url)
    time.sleep(2)
    html = driver.page_source

    allLinks = self.parseHtml(html)
    self.allLinks = allLinks

    for link in allLinks:
      if UrlUtils.isAppendCondition(arr = innerLinks, link = link) :
        self.newInnerLinks.append(link.attrs['href'])

      if UrlUtils.isAppendCondition(arr = gtpLinks, link = link) and UrlUtils.isAppendCondition(arr = innerLinks, link = link):
        self.newgtpLinks.append(link.attrs['href'])

    self.newInnerLinks = joinList(self.newInnerLinks, self.innerLinks)
    self.newgtpLinks = joinList(self.newgtpLinks, self.gtpLinks)
    return
