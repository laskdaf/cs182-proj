import os
import json
import operator
from gensim import corpora
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
from collections import defaultdict

def getCategoricalTokens(data):
    tokens = []

    tokens.append('Tok-FurLength-' + str(data['FurLength']))
    tokens.append('Tok-Color1-' + str(data['Color1']))
    tokens.append('Tok-Fee-' + str(0 if data['Fee'] == 0 else 1))
    tokens.append('Tok-Vaccinated-' + str(data['Vaccinated']))
    tokens.append('Tok-Dewormed-' + str(data['Dewormed']))
    tokens.append('Tok-Sterilized-' + str(data['Sterilized']))
    tokens.append('Tok-MaturitySize-' + str(data['MaturitySize']))
    tokens.append('Tok-Quantity-' + str(1 if data['Quantity'] == 1 else 2))
    tokens.append('Tok-PhotoAmt-' + str(int(data['PhotoAmt']//5)))
    tokens.append('Tok-Gender-' + str(data['Gender']))
    tokens.append('Tok-Age-' + str(data['Age']//12))
    # tokens.append('Tok-Breed1-' + str(data['Breed1']))
    tokens.append('Tok-Breed2-' + str(0 if data['Breed2'] == 0 else 1))

    return tokens

directory = 'json_with_labels_all'

all_tokens = []

for filename in os.listdir(directory):

    id = filename.split(".")[0].split("_")[-1]

    with open(directory + '/' + filename) as json_file:
        data = json.load(json_file)

        all_tokens.extend(getCategoricalTokens(data))

freq = {}

for tok in all_tokens:
    if tok not in freq:
        freq[tok] = 0

    freq[tok] += 1

freq = dict(sorted(freq.items(), key=operator.itemgetter(1), reverse=True))

print(freq)
print(len(freq))
