import shutil
import glob
import os
from pathlib import Path

class FileManager: 

    def __init__(self):
        self.downloadsPath = str(os.path.join(Path.home(), "Downloads"))
        self.destinationPath = os.path.dirname(os.path.abspath(__file__)) + '/downloadedFiles/'
        self.wordsPath = os.path.dirname(os.path.abspath(__file__)) + '/words.txt'

    def read_all_words(self):
        with open(self.wordsPath) as f:
            lines = f.readlines()
        return lines

    def create_folder(self, folderName):
        path = self.destinationPath + "/" + folderName
        if os.path.exists(path) == False:
            os.mkdir(path)

    def is_download_finished(self):
        if any([filename.endswith(".crdownload") for filename in os.listdir(self.downloadsPath)]):
            return False
        else:
            return True
        
    def has_file(self, fileName, folderName):
        targetPath = self.destinationPath + "/" + folderName
        if any([filename.endswith(fileName + ".zip") for filename in os.listdir(targetPath)]):
            return True
        else:
            return False

    def cut_and_paste_last_file(self, folderName, newFileName):
        
        # find last downloaded
        files = os.listdir(self.downloadsPath)
        paths = [os.path.join(self.downloadsPath, basename) for basename in files]
        lastFile = max(paths, key = os.path.getctime)
        
        # it should be .zip file
        if lastFile.find(".zip") != -1:
            
            # change name
            newName = self.downloadsPath + "/" + newFileName + ".zip"
            os.rename(lastFile, newName)
            
            targetPath = self.destinationPath + "/" + folderName

            # move it to destination path
            if os.path.exists(targetPath + "/" + newFileName + ".zip" ) == False:
                shutil.move(newName, targetPath)
            else:
                os.remove(newName)
                print("object already exist")