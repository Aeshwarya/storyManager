import tempfile
from .. import settings

class FileStore:
    currentFileIndex = 0

    def __init__(self):
        self.fileStoreDirectory = settings.FILE_STORE_PATH
        print(self.fileStoreDirectory)

    def storeFileAndGetLocation(self, file, extension):
        filePath = self.fileStoreDirectory + str(FileStore.currentFileIndex) + extension
        file.save(filePath)
        FileStore.currentFileIndex = FileStore.currentFileIndex + 1
        return filePath