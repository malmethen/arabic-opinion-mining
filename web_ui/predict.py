import re
import string
from emoji import replace_emoji
from pyarabic.araby import strip_tatweel, normalize_teh, strip_diacritics, normalize_hamza
from split_waw_arabic.process_waw_rooting import separate_waw

def clean_text(data):
    """ Removes any unnecessary characters including emojis, english words, and numbers. """

    data = strip_tatweel(data)
    data = replace_emoji(data, replace=' ')
    data = data.replace('\u200f', ' ')
    data = data.replace('\u061c', ' ')
    data = data.replace('\u2026', ' ')
    data = data.replace('\u2066', ' ')
    data = data.replace('\u2069', ' ')
    data = data.replace('\u200e', ' ')
    data = data.replace('\n', ' ')
    data = re.sub('[a-zA-Z0-9]', ' ', data)
    data = re.sub('[٠-٩]', ' ', data)
    data = data.replace('ﷺ', ' ')
    data = " ".join(data.split())

    return data

def remove_punctuations(data):
    """ Removes punctuations. """

    ara_punc = '''`÷×؛<>_()*&^%][ـ،/:"؟.,﴾﴿’'{}~¦+|!”…“–ـ'''
    eng_punc = string.punctuation
    punc_list = ara_punc + eng_punc

    for char in data:
        if char in punc_list:
            data = data.replace(char, ' ')
    data = " ".join(data.split())

    return data

def remove_duplicates(data):
    """ Detects 3 or more duplicate letters and removes the extra letters. """

    data = re.sub(r'(.)\1{2,}', r'\1', data)

    return data

def split_waw(data):
    """ Splits the conjunction Waw by getting the root of the word to check if Waw is original or not. """

    data = separate_waw(data)
    
    return data

def normalize_text(data):
    """ Prevents inconsistent spelling across data to imporve accuracy. """

    data = re.sub("[إأآا]", "ا", data)
    data = normalize_teh(data)
    data = strip_diacritics(data) 
    data = normalize_hamza(data)
    data = re.sub("گ", "ك", data)

    return data

def data_pipeline(data):
    data = clean_text(data)
    data = remove_punctuations(data)
    data = remove_duplicates(data)
    data = split_waw(data)
    data = normalize_text(data)
    #print(data)
    
    return data