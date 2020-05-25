import tempfile
from .. import settings
import uuid

class FileStore:
    # currentFileIndex = 0

    def __init__(self):
        self.fileStoreDirectory = settings.FILE_STORE_PATH
        print(self.fileStoreDirectory)

    def storeFileAndGetLocation(self, file, extension):
        filePath = self.fileStoreDirectory + str(uuid.uuid4()) + extension
        print(filePath)
        file.save(filePath)
        # FileStore.currentFileIndex = FileStore.currentFileIndex + 1
        return filePath