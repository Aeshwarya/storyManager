class BaseService:
    __abstract__  = True
    
    def __init__(self, app):
        self.app = app

