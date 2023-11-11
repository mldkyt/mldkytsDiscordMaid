
import json
import os

def init_lang_prefs():
    with open('data/user_lang_prefs.json', 'w') as f:
        json.dump({}, f)

def get_user_lang(id: int):
    with open('data/user_lang_prefs.json') as f:
        prefs = json.load(f)
        
    if str(id) in prefs:
        return prefs[str(id)]
    
    return 'en'

def set_user_lang(id: int, lang: str):
    with open('data/user_lang_prefs.json') as f:
        prefs = json.load(f)
        
    prefs[str(id)] = lang
    
    with open('data/user_lang_prefs.json', 'w') as f:
        json.dump(prefs, f)

def get_string(key: str, lang: str = 'en') -> str:
    with open('languages/language_%s.json' % lang) as f:
        file = json.load(f)

    if key in file:
        return file[key]
    else:
        # try to get the string from the english file
        with open('languages/language_en.json') as f:
            file = json.load(f)
        if key in file:
            return file[key] + ' (missing {} translation)'.format(lang)
    
    return 'str.%s.%s' % (lang, key)

def get_languages() -> list:
    langs = []
    for file in os.listdir('languages'):
        if file.startswith('language_') and file.endswith('.json'):
            langs.append(file[9:-5])
            
    return langs
