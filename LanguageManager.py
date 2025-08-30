import json
from pathlib import Path
import os
from Language import Language
from LanguagePair import LanguagePair


class LanguageManager:
    base_dir = Path(__file__).resolve().parent

    def __init__(self):
        self.translations = None
        self.code_to_pair = None
        self.pairs = None
        self.code_to_lang = None
        self.languages = None



    def load_languages(self):
        data_dir = os.path.join(self.base_dir,'Data')
        with open(os.path.join(data_dir,'languages.json'),encoding='utf-8') as file:
            languages = json.load(file)
            
        self.languages = []
        with open(os.path.join(data_dir, 'translations.json'), encoding='utf-8') as file:
            self.translations = json.load(file)
        self.code_to_lang = {}
        

        for l in languages:
            lang = Language(l,languages[l])
            self.code_to_lang[l] = lang 
            self.languages.append(lang)
        

        dirs = os.listdir(data_dir)
        dirs.remove('languages.json')
        dirs.remove('translations.json')
        self.pairs = []
        
        self.code_to_pair = {}
        for d in dirs:
            s = d.split('_')
            from_lang = self.code_to_lang[s[0]]
            to_lang = self.code_to_lang[s[1]]
            path = os.path.join(data_dir,d)
            pair = LanguagePair(from_lang,to_lang,path,d)
            self.pairs.append(pair)
            self.code_to_pair[d] = pair
    def get_available_pairs(self,user_lang):
        pairs = []

        for p in self.pairs:
            pairs.append((p.from_lang.translations[user_lang],p.to_lang.translations[user_lang],p.code))
        return pairs
    def filter(self,lang,user_lang):
        code = None
        for l in self.languages:
            if code is not None:
                break
            for t in l.translations:
                if lang == l.translations[t]:
                    code = l.code
                    break
        if code is not None:
            result = []
            for p in self.pairs:
                if p.from_lang.code == code or p.to_lang.code == code:
                    result.append((p.from_lang.translations[user_lang], p.to_lang.translations[user_lang], p.code))
            return result
    def get_available_langs(self,user_lang):
        result = []
        for l in self.languages:
            result.append(l.translations[user_lang])
        return result
    def get_text(self,user_lang_code,code):
        return self.translations[user_lang_code][code]
    def get_available_user_langs(self):
        result = []
        for t in self.translations:
            lang = self.code_to_lang[t]
            result.append((t,lang.name))
        return result
    def get_user_lang(self,code):
        return self.code_to_lang[code].translations['English']



    # Ln = LanguageManager()
# print(Ln.base_dir)
# Ln.load_languages()
# print(Ln.languages[0])
# print(Ln.get_available_pairs('Russian'))