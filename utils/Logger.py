from utils.UrlUtils import UrlUtils

class Logger:
  @staticmethod
  def categoryInfo(internalLinks, categoryList):
    count = 0
    for subUrlTag in categoryList:
      subUrlData = [link for link in internalLinks if UrlUtils.isSubUrl(link, subUrlTag)]
      count += len(subUrlData)
      print("[CATE]       {0} {1} " .format(subUrlTag,len(subUrlData)))
    
    print("[CATE]       other: {0}".format(len(internalLinks)- count))