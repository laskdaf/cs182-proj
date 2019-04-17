import os
import json

directory = 'json_with_labels'
destination = 'text_and_label'

try:
    os.mkdir(destination)
except OSError:
    print ("Creation of the directory failed")
else:
    print ("Successfully created the directory")

output = {}

for filename in os.listdir(directory):

    id = filename.split(".")[0].split("_")[-1]

    # print(id)

    with open(directory + '/' + filename) as json_file:
        data = json.load(json_file)

        # stitch together sentences
        sentence = ""
        for s in data['sentences']:
            sentence += s['text']['content'] + ' '
        data['fullText'] = sentence[:-1]

    output[id] = data

with open(destination + "/json_complete.json", 'w') as outfile:
    json.dump(output, outfile, indent=4)

# print(output[0])
