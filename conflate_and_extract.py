import os
import json
from gensim import corpora
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
from collections import defaultdict

stop = stopwords.words('english')# + list(string.punctuation)
punctuation = set(list(list(string.punctuation)))

# extract and tokenize categorical data into a list
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

# cleans text by removing (1) stop words and punctuation
def cleanText(text):
    unpunctuated_text = "".join([c for c in text if c not in punctuation])
    return [i for i in word_tokenize(unpunctuated_text.lower()) if i not in stop]

# get a token to int mapping for the numWords most frequent words
def dictionaryFromTexts(texts, numWords):
    # get the frequencies of the words
    frequency = defaultdict(int)
    for text in texts:
        for token in text:
            frequency[token] += 1

    # only use the top numWords-1 words (reserve 1 for the unkown token)
    frequency = dict(sorted(frequency.items(), key=lambda kv: kv[1], reverse=True)[:numWords - 1])
    tokenized_texts = [[token for token in text if token in frequency and frequency[token] > 1] for text in texts]

    return corpora.Dictionary(tokenized_texts)

stop = stopwords.words('english') + list(string.punctuation)

directory = 'json_with_labels_all'
destination = 'text_and_label_all'

# try:
#     os.mkdir(destination)
# except OSError:
#     print ("Creation of the directory failed")
# else:
#     print ("Successfully created the directory")

output = {}
texts = []
categorical_labels = []

for filename in os.listdir(directory):

    id = filename.split(".")[0].split("_")[-1]

    with open(directory + '/' + filename) as json_file:
        data = json.load(json_file)

        # stitch together sentences
        sentence = ""
        for s in data['sentences']:
            sentence += s['text']['content'] + ' '
        data['fullText'] = sentence[:-1]

        cleanedText = cleanText(data["fullText"])
        texts.append(cleanedText)

        categorical_labels.append(getCategoricalTokens(data))

    output[id] = data

dictionary = dictionaryFromTexts(texts, 5000)
dictionary.add_documents(categorical_labels)
# dictionary.save(os.path.join(TEMP_FOLDER, 'deerwester.dict'))  # store the dictionary, for future reference
# print(dictionary)
print(dictionary.token2id)

# new_doc = "Human computer interaction"
# for w in new_doc.lower().split():
#     new_vec = dictionary.doc2bow([w])
#     print(new_vec)

maxLen = 0

for key, value in output.items():
    fullText = value["fullText"]

    vectorized = []

    for w in fullText.lower().split()[:500] + getCategoricalTokens(value):
        vec = dictionary.doc2bow([w])
        word_id = 0
        if len(vec) > 0:
            word_id = vec[0][0] + 1

        vectorized.append(word_id)

    output[key]["vectorized"] = vectorized
    maxLen = max(maxLen, len(vectorized))

print(output["bef897b2b"])
print(maxLen)

with open(destination + '/json_vectorized_categorical.json', 'w') as outfile:
    json.dump(output, outfile, indent=4)
