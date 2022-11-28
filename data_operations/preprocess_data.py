import json
import re
from split_waw_arabic.process_waw_rooting import separate_waw
from arabicstopwords.arabicstopwords import is_stop
from pyarabic.araby import tokenize, normalize_teh, strip_diacritics, normalize_hamza

data_file = open('dataset.json')
data = json.load(data_file)

def remove_duplicates():
    """ Detects 3 or more duplicate letters and removes the extra letters. """

    for i in range(len(data)):
        data[i]['text'] = re.sub(r'(.)\1{2,}', r'\1', data[i]['text'])
    
    with open('dataset.json', 'w') as ds_write:
        ds_write.write(json.dumps(data, ensure_ascii= False))

def split_waw():
    """ Splits the conjunction Waw by getting the root of the word to check if Waw is original or not. """

    for i in range(len(data)):
        data[i]['text'] = separate_waw(data[i]['text'])

    with open('dataset.json', 'w') as ds_write:
        ds_write.write(json.dumps(data, ensure_ascii= False))

def normalize_text():
    """ Prevents inconsistent spelling across data to imporve accuracy. """

    for i in range(len(data)):
        data[i]['text'] = re.sub("[إأآا]", "ا", data[i]['text'])
        data[i]['text'] = normalize_teh(data[i]['text'])
        data[i]['text'] = strip_diacritics(data[i]['text']) 
        data[i]['text'] = normalize_hamza(data[i]['text'])
        data[i]['text'] = re.sub("گ", "ك", data[i]['text'])
    
    with open('dataset.json', 'w') as ds_write:
        ds_write.write(json.dumps(data, ensure_ascii=False))

def tokenize_words():
    for i in range(len(data)):
        data[i]['text'] = tokenize(data[i]['text'])
    
    with open('dataset.json', 'w') as ds_write:
        ds_write.write(json.dumps(data, ensure_ascii=False))

def join_text():
    """ Combines tokenized text in one string. """

    for i in range(len(data)):
        data[i]['text'] = ' '.join(data[i]['text'])

    with open('dataset.json', 'w') as ds_write:
        ds_write.write(json.dumps(data, ensure_ascii=False))
    
# remove_duplicates()
# split_waw()
# normalize_text()
# tokenize_words()
# join_text()

data_file.close()
