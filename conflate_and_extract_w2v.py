import os
import json
from gensim.models import KeyedVectors
from nltk import word_tokenize
from nltk.corpus import stopwords
import string

stop = stopwords.words('english')# + list(string.punctuation)
punctuation = set(list(list(string.punctuation)))


# Load Google's pre-trained Word2Vec model.
model = KeyedVectors.load_word2vec_format('./w2v_model/GoogleNews-vectors-negative300.bin', binary=True)

# cleans text by removing (1) stop words and punctuation
def cleanText(text):
    unpunctuated_text = "".join([c for c in text if c not in punctuation])
    return [i for i in word_tokenize(unpunctuated_text.lower()) if i not in stop]

directory = 'json_with_labels_all'
destination = 'text_and_label_all'

# try:
#     os.mkdir(destination)
# except OSError:
#     print ("Creation of the directory failed")
# else:
#     print ("Successfully created the directory")

output = {}
maxLen = 0

for filename in os.listdir(directory):

    id = filename.split(".")[0].split("_")[-1]

    with open(directory + '/' + filename) as json_file:
        data = json.load(json_file)

        # stitch together sentences
        sentence = ""
        for s in data['sentences']:
            sentence += s['text']['content'] + ' '
        data['fullText'] = sentence[:-1]

        seq = []
        for w in cleanText(data["fullText"]):
            if w in model.wv:
                seq.append(model.wv[w].tolist())

        data["vectorized"] = seq
        maxLen = max(maxLen, len(seq))

        output[id] = data

print(output["bef897b2b"])

with open(destination + '/json_w2v.json', 'w') as outfile:
    json.dump(output, outfile, indent=4)
