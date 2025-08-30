import os
import random
class Vocab:
    def __init__(self,path):
        self.path = path
        self.themes = {}
        files = os.listdir(path)
        for f in files:
            file_path = os.path.join(path,f)
            translations = []
            with open(file_path,encoding='utf-8') as file:
                for l in file.readlines():
                    s = l.strip().split(';')
                    variants_from = s[0].split(',')
                    variants_to = s[1].split(',')
                    for vf in variants_from:
                        for vt in variants_to:
                            translations.append((vf,vt))
                self.themes[f] = translations
    def random_pair(self,theme) -> tuple[str,str]:
        return random.choice(self.themes[theme])
    def generate_variants(self,theme,count,ignore):
        res = [ignore]
        while len(res) < count:
            item = self.random_pair(theme)[1]
            if item != ignore and item not in res:
                res.append(item)
        random.shuffle(res)
        return res
    def check(self,theme,first_word,text):
        for t in self.themes[theme]:
            if t[0] == first_word and t[1] == text:
                return True
        return False




