from parse import parse

class PdmTest:
    def __init__(self, name:str, version:str) -> None:
        self.__name = name
        self.__version = version
        
    @property
    def name(self):
        return self.__name
    
    @property
    def version(self):
        return self.__version
    
    def mod_name(self,name: str):
        self.name = name
        
    def mod_version(self,version: str):
        self.version = version
        
    def details(self)->str:
        print(f'Details: \nName: {self.name}\nVersion: {self.version}')
        
class Identical:
    def __init__(self, model:str, value:str, model_personalize: dict = None) -> None:
        self.__value = value
        self.__model = model
        self.__model_personalize = model_personalize
        
    def getValidate(self):
        values = parse(self.__model, self.__value, self.__model_personalize)
        if values is not None:
            return True
        else:
            return False
        
    def getData(self):
        values = parse(self.__model, self.__value, self.__model_personalize)
        if values is not None:
            return values.named
        else:
            return False