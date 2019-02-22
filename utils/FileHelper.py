class FileHelper:
  @staticmethod
  def writeToFile(str, path):
    text_file = open(path, "w")
    text_file.write(str)
    text_file.close()

  @staticmethod
  def readFileToList(path):
    text_file = open(path, "r")
    return text_file.read().splitlines()
