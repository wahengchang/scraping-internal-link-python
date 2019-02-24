import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from utils.FileHelper import FileHelper
from utils.UrlUtils import UrlUtils

def joinList(arr1 = [], arr2 = []):
  return list(set( arr1 + arr2 ))

class Scraper:
  def __init__(self, url, innerLinks = [], gtpLinks = [], options = {}):

    self.url = url
    self.allAtagss = []
    self.allLinks = []
    self.innerLinks = innerLinks
    self.gtpLinks = gtpLinks
    self.options = options
    self.newInnerLinks = []
    self.newgtpLinks = []

  def parseHtml(self, html):
    bs = BeautifulSoup(html, 'html.parser')
    return bs.find_all('a')

  def preFetchHtml(self, driver):
    return

  def fetchHtml (self):
    url =  '{0}{1}'.format(self.options["domain"], self.url) if self.url.startswith('/') else self.url
    driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME)

    driver.get(url)
    print('[INFO] processing %s' % url)
    time.sleep(2)
    self.preFetchHtml(driver)
    html = driver.page_source
    driver.quit()
    return html

  # @staticmethod
  def processLinks(self):
    print('[INFO] processLinks %s' % self.url)

    innerLinks = self.innerLinks
    gtpLinks = self.gtpLinks

    html = self.fetchHtml()

    allAtags = self.parseHtml(html)
    self.allAtags = allAtags


    self.allLinks = []
    for item in allAtags:
      if hasattr(item.attr, 'href'):
        self.allLinks.append(item.attrs['href'])

    self.allLinks = joinList(self.allLinks, []) # unique

    self.newInnerLinks = list(filter(lambda link: UrlUtils.isAppendCondition(arr = innerLinks, link = link), self.allLinks))
    self.newgtpLinks = list(filter(
      lambda link: UrlUtils.isAppendCondition(arr = gtpLinks, link = link) and UrlUtils.isAppendCondition(arr = innerLinks, link = link)
      , self.allLinks))


    # for link in self.allLinks:
    #   if UrlUtils.isAppendCondition(arr = innerLinks, link = link) :
    #     self.newInnerLinks.append(link.attrs['href'])

    #   if UrlUtils.isAppendCondition(arr = gtpLinks, link = link) and UrlUtils.isAppendCondition(arr = innerLinks, link = link):
    #     self.newgtpLinks.append(link.attrs['href'])

    self.newInnerLinks = joinList(self.newInnerLinks, self.innerLinks)
    self.newgtpLinks = joinList(self.newgtpLinks, self.gtpLinks)
    return
