import os
import json
from gensim import corpora
from nltk import word_tokenize
from nltk.corpus import stopwords
import string
from collections import defaultdict


stop = stopwords.words('english') + list(string.punctuation)

filename = 'text_and_label/json_complete.json'

documents = []

with open(filename) as json_file:
    data = json.load(json_file)

    for key, value in data.items():
        fullText = value["fullText"]

        cleanedText = [i for i in word_tokenize(fullText.lower()) if i not in stop]

        documents.append(cleanedText)

texts = documents

# print(texts[0])

frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1

texts = [[token for token in text if frequency[token] > 1] for text in texts]

dictionary = corpora.Dictionary(texts)
# dictionary.save(os.path.join(TEMP_FOLDER, 'deerwester.dict'))  # store the dictionary, for future reference
# print(dictionary)
print(dictionary.token2id)



# new_doc = "Human computer interaction"
# for w in new_doc.lower().split():
#     new_vec = dictionary.doc2bow([w])
#     print(new_vec)

data = None

with open(filename) as json_file:
    data = json.load(json_file)

    for key, value in data.items():
        fullText = value["fullText"]

        embedding = []

        for w in fullText.lower().split():
            vec = dictionary.doc2bow([w])
            word_id = 0
            if len(vec) > 0:
                word_id = vec[0][0] + 1

            embedding.append(word_id)

        data[key]["embedding"] = embedding

print(data["bef897b2b"])

with open('text_and_label/json_embedding.json', 'w') as outfile:
    json.dump(data, outfile, indent=4)
