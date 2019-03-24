import time
import re
from pathlib import Path

from utils.FileHelper import FileHelper
from utils.Scraper.ScraperScroll import ScraperScroll
from utils.UrlUtils import UrlUtils
from utils.Logger import Logger
from config import Config

startTime = time.time()
TARGET_DOMAIN = Config.TARGET_DOMAIN
COOKIES = getattr(Config, 'COOKIES', [])

PROJECT_NAME = Config.PROJECT_NAME
CATEGORY_LIST = Config.CATEGORY_LIST
PATH_RESULT = './temp/%s_result.txt' % PROJECT_NAME  #result
PATH_GTP = './temp/%s_gtp.txt' % PROJECT_NAME        #going to parse

def init():
  if not Path(PATH_RESULT).is_file():
    FileHelper.writeToFile('\n'.join([]), PATH_RESULT)

  if not Path(PATH_GTP).is_file():
    FileHelper.writeToFile('\n'.join([]), PATH_GTP)
    print('[INFO] going to process %s' % TARGET_DOMAIN)
    processUrl(TARGET_DOMAIN)

    for subUrlTag in CATEGORY_LIST:
      processUrl('{0}/{1}'.format(TARGET_DOMAIN, subUrlTag))

def processUrl(__url):
  options= {
    "domain": TARGET_DOMAIN,
    "saveHtml": Config.SAVE_HTML if hasattr(Config, 'SAVE_HTML') else False
  }

  sp = ScraperScroll(
    url = __url, 
    innerLinks = FileHelper.readFileToList(PATH_RESULT), 
    gtpLinks = FileHelper.readFileToList(PATH_GTP), 
    options = options,
    cookies = COOKIES
  )

  sp.processLinks()

  print('[INFO] Found %d new allLinks' % len(sp.allLinks))
  # for newlink in sp.allLinks:
  #   print(newlink)
  print('[INFO] Found %d new newInnerLinks' % len(sp.newInnerLinks))
  print('[INFO] Found %d new newgtpLinks' % len(sp.newgtpLinks))

  Logger.categoryInfo(sp.newInnerLinks, CATEGORY_LIST)
  sp.newgtpLinks.sort(reverse=True)
  FileHelper.writeToFile('\n'.join(sp.newInnerLinks), PATH_RESULT)
  FileHelper.writeToFile('\n'.join(sp.newgtpLinks), PATH_GTP)

def processNext():
  goingToProcessLinks = FileHelper.readFileToList(PATH_GTP)
  if len(goingToProcessLinks) <= 0:
    print('[DONE] no more gtp links')
    return

  link = goingToProcessLinks[0]
  processUrl(link)

  goingToProcessLinks.remove(link)
  FileHelper.writeToFile('\n'.join(goingToProcessLinks), PATH_GTP)
  print('[INFO]   %d links need to be processed' % len(goingToProcessLinks))
  return processNext()

init()
processNext()