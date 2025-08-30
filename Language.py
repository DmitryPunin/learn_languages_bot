import json
class Language:
    def __init__(self,code,translations:dict):
        self.code = code
        self.name = translations[translations['English']]
        self.translations = translations


