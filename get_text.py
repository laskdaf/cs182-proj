import os
import json
import pandas as pd
from collections import defaultdict
from gensim import corpora

stoplist = set('for a of the and to in'.split())

directory = './json_with_labels/'

frequency = defaultdict(int)
vocab = []


# try:  
#     os.mkdir(destination)
# except OSError:  
#     print ("Creation of the directory %s failed")
# else:  
#     print ("Successfully created the directory %s ")

#  and filename == 'with_label_0a0e8c15b.json'
for filename in os.listdir(directory):
    if filename.endswith(".json"):
        with open(directory + filename, 'r+') as json_file:
            data = json.load(json_file)
            
            sentences = data["sentences"]
            
            # print(len(sentences))
            # print(sentences)

            raw_content = ""
            for s in sentences:
                text = s['text']
                content = text['content'] + ' '
                # print(content)
                # print(type(content))
                raw_content += content
            
            words = raw_content.split(" ")
            words = [str(w) for w in words]
            for word in words:
                if word not in stoplist:
                    frequency[word] += 1
                    
            filtered = [w for w in words if frequency[w] > 1]
            vocab.append(filtered)
                

            print(len(words))
            print(words)
            # if len(words) > 30:
            #     print(raw_content)
            #     break
            data['raw_content'] = raw_content
            # json_file.seek(0)
            # json.dump(data, json_file, indent=4)

            # pet_hash = filename[:-5]
            # query = pet_data[pet_data['PetID']==pet_hash]
            # print(pd.to_numeric(query["Type"]))
            # print(type(pd.to_numeric(query["Type"])))
            
            # # not a dog
            # if (query["Type"].item() != 1):
            #     continue
                
            # # add label to json file
            # label = query['AdoptionSpeed'].item()
            # data['label'] = label
            
            # with open('./' + destination + "/with_label_" + filename, 'w') as outfile:
            #     json.dump(data, outfile, indent=4)

print(vocab)

dictionary = corpora.Dictionary(vocab)


dictionary.save('/tmp/deerwester.dict')  # store the dictionary, for future reference
print(dictionary)

print(dictionary.token2id)

print(len(dictionary.token2id))
