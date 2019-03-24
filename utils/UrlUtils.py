from config import Config
TARGET_DOMAIN = Config.TARGET_DOMAIN

validLetters = "abcdefghijklmnopqrstuvwxyz1234567890"

class UrlUtils:
  @staticmethod
  def isSubUrl(link, subUrl, domain = TARGET_DOMAIN):
    if link.startswith('{domain}/{subUrl}'.format(domain = domain, subUrl= subUrl)):
      return True
    else :
      return False

  @staticmethod
  def isSameDomain(url, domain = TARGET_DOMAIN):
    if url.startswith(domain):
      return True
    if url.startswith('/'):
      return True
    return False
    
  @staticmethod
  def isAppendCondition(arr,link,domain = TARGET_DOMAIN):

    def isEmail(_link):
      return 'mailto' in _link
    def isEmpty(_link):
      return '#' == _link
    def isRepeat(_arr, _link):
      return _link in _arr
      
    try:
      if not isRepeat(arr, link) and not isEmail(link) and not isEmpty(link) and UrlUtils.isSameDomain(link):
        return True
      else :
        return ''
    except:
      return ''

  @staticmethod
  def onlyAzAndDigit(str):
    newString = ''
    for char in str:
      if char in validLetters:
          newString += char
    return newString