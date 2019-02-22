from config import Config
TARGET_DOMAIN = Config.TARGET_DOMAIN

class UrlUtils:
  @staticmethod
  def isSubUrl(link, subUrl, domain = TARGET_DOMAIN):
    if link.startswith('{domain}/{subUrl}'.format(domain = domain, subUrl= subUrl)):
      return True
    else :
      return False
    
  @staticmethod
  def isAppendCondition(arr,link,domin = TARGET_DOMAIN):
    try:
      url = link.attrs['href']
      if 'href' in link.attrs and url not in arr and 'mailto' not in url and '#' != url and url.startswith(domin):
        return True
      else :
        return False
    except:
      return False