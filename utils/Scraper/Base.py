import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from utils.UrlUtils import UrlUtils

def joinList(arr1 = [], arr2 = []):
  return list(set( arr1 + arr2 ))

def getHref(aTagObject):
  try:
    if hasattr(aTagObject.attr, 'href') or aTagObject.attrs['href']:
      return aTagObject.attrs['href']
    
    return ''
  except:
    return ''

class Scraper:
  def __init__(self, url, innerLinks = [], gtpLinks = [], cookies= [], options = {}):

    self.url = url
    self.allAtagss = []
    self.allLinks = []
    self.innerLinks = innerLinks
    self.gtpLinks = gtpLinks
    self.options = options
    self.cookies = cookies
    self.newInnerLinks = []
    self.newgtpLinks = []

  def parseHtml(self, html):
    bs = BeautifulSoup(html, 'html.parser')
    return bs.find_all('a')
    
  def afterParseAllLinks(self, allLinks):
    return self.allLinks

  def afterFetchHtml(self, driver):
    return

  def initCookie (self, driver, url):
    driver.get(url)
    driver.delete_all_cookies()

    cookies = self.cookies

    if len(cookies) >= 1:
      for c in cookies:
        driver.add_cookie({'name': c[0],'value': c[1]})

    return


  def fetchHtml (self):
    domain = self.options["domain"]
    saveHtml = self.options["saveHtml"]
    _url = self.url
    url =  '{0}{1}'.format(domain, _url) if _url.startswith('/') else _url
    driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub", DesiredCapabilities.CHROME)

    self.initCookie(driver, url)

    driver.get(url)
    print('[INFO] processing %s' % url)
    time.sleep(2)
    self.afterFetchHtml(driver)
    html = driver.page_source
    driver.quit()

    if saveHtml :
      f = open(UrlUtils.onlyAzAndDigit(domain) + '.html','a')
      f.write(html)
      f.close()

    return html

  # @staticmethod
  def processLinks(self):
    print('[INFO] processLinks %s' % self.url)

    innerLinks = self.innerLinks
    gtpLinks = self.gtpLinks

    html = self.fetchHtml()

    allAtags = self.parseHtml(html)
    self.allAtags = allAtags

    print('-=-=-=-= 1 -=-=-=-=')
    # print(allAtags)

    self.allLinks = []
    for item in allAtags:
      href = getHref(item)

      if href and href.strip(): # not empty string
        self.allLinks.append(href)

    self.allLinks = joinList(self.allLinks, []) # unique
    self.allLinks = self.afterParseAllLinks(self.allLinks)

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
