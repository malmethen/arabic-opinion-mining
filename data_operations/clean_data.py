import json
import re
import string
from emoji import replace_emoji
from pyarabic.araby import strip_tatweel
from operator import itemgetter

data_file = open('dataset.json')
data = json.load(data_file)

dataset = []

def init_processing():
    """ Extracts 'test' and 'stars' columns, adds a 'sentiment' column and dumps everything into a json file. """
   
    for entry in data:
        text = entry['text']
        stars = entry['stars']
        
        temp = {
            'text': text,
            'stars': stars
        }

        dataset.append(temp)

    with open('dataset.json', 'w') as ds_write:
        ds_write.write('[')
        ds_write.write('\n')
        for i in range(len(dataset)):
            ds_write.write('{')
            ds_write.write('"text": ' + json.dumps(dataset[i]['text'], ensure_ascii= False))
            ds_write.write(', ')
            ds_write.write('"stars": ' + json.dumps(dataset[i]['stars']))
            ds_write.write(', ')

            if dataset[i]['stars'] <= 2:
                ds_write.write('"sentiment": "negative"')
            
            if dataset[i]['stars'] == 3:
                ds_write.write('"sentiment": "neutral"')
            
            if dataset[i]['stars'] >= 4:
                ds_write.write('"sentiment": "positive"')
            
            ds_write.write('}')
            ds_write.write(',')
            ds_write.write('\n')
        ds_write.write(']')

def del_empty_reviews():
    """ Loops over each item and deletes empty reviews. """
    
    i = 0
    while i < len(data): 
        text = data[i]['text']
        if text == None or text == "":
            del data[i]
            i = i - 1
        i = i + 1

    with open('dataset.json', 'w') as ds_write:
        ds_write.write(json.dumps(data, ensure_ascii= False))
    
    print(len(data))

def clean_text():
    """ Removes any unnecessary characters including emojis, english words, and numbers. """
    
    for i in range(len(data)):
        data[i]['text'] = strip_tatweel(data[i]['text'])
        data[i]['text'] = replace_emoji(data[i]['text'], replace=' ')
        data[i]['text'] = data[i]['text'].replace('\u200f', ' ')
        data[i]['text'] = data[i]['text'].replace('\u061c', ' ')
        data[i]['text'] = data[i]['text'].replace('\u2026', ' ')
        data[i]['text'] = data[i]['text'].replace('\u2066', ' ')
        data[i]['text'] = data[i]['text'].replace('\u2069', ' ')
        data[i]['text'] = data[i]['text'].replace('\u200e', ' ')
        data[i]['text'] = data[i]['text'].replace('\n', ' ')
        data[i]['text'] = re.sub('[a-zA-Z0-9]', ' ', data[i]['text'])
        data[i]['text'] = re.sub('[٠-٩]', ' ', data[i]['text'])
        data[i]['text'] = data[i]['text'].replace('ﷺ', ' ')
        data[i]['text'] = " ".join(data[i]['text'].split())

    with open('dataset.json', 'w') as ds_write:
        ds_write.write(json.dumps(data, ensure_ascii= False))

def remove_punctuations():
    """ Removes punctuations. """

    ara_punc = '''`÷×؛<>_()*&^%][ـ،/:"؟.,﴾﴿’'{}~¦+|!”…“–ـ'''
    eng_punc = string.punctuation
    punc_list = ara_punc + eng_punc

    for i in range(len(data)):
        for char in data[i]['text']:
            if char in punc_list:
                data[i]['text'] = data[i]['text'].replace(char, ' ')
        data[i]['text'] = " ".join(data[i]['text'].split())
    
    with open('dataset.json', 'w') as ds_write:
        ds_write.write(json.dumps(data, ensure_ascii= False))

def merge_files():
    """ In case of multiple json files, this function combines them into a single json file. """

    data = data1 + data2

    with open('dataset_final.json', 'w') as ds_write:
        ds_write.write(json.dumps(data, ensure_ascii= False))
    
    print(len(data))

def sort_items():
    """ Sorts the reviews in descending order. """

    sorted_data = sorted(data, key=itemgetter('stars'), reverse=True)

    with open('dataset_old.json', 'w') as ds_write:
        ds_write.write(json.dumps(sorted_data, ensure_ascii= False))

def count():
    """ Counts number of reviews. """
    print(len(data)) # 5693

    pos_reviews = sum(x.get("sentiment") == "positive" for x in data) 
    print(pos_reviews) # 2465

    neu_reviews = sum(x.get("sentiment") == "neutral" for x in data)
    print(neu_reviews) # 741

    neg_reviews = sum(x.get("sentiment") == "negative" for x in data)
    print(neg_reviews) # 2487

# init_processing()
# del_empty_reviews()
# clean_text()
# remove_punctuations()
# merge_files()
# sort_items()
# count()

data_file.close()