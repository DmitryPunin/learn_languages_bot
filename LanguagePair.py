from Language import Language
from Vocab import Vocab
import os
class LanguagePair:
    def __init__(self,from_lang,to_lang,path,code):
        self.from_lang = from_lang
        self.to_lang = to_lang
        self.path = path
        self.code = code
        self.init_vocabs()
    def init_vocabs(self):
        self.vocab = Vocab(os.path.join(self.path,'vocab'))
        self.sentences = Vocab(os.path.join(self.path,'sentences'))
    def translate(self,user_lang):
        return (self.from_lang.translations[user_lang],self.to_lang.translations[user_lang])



