# script to transform csv all_text.txt, to a list of path 
# filter on keywords

from tqdm import tqdm


with open('all_texts.txt', 'r') as f:
    data = f.readlines()
paths = []
for line in tqdm(data):
    try:
        paths.append(line.split(' ')[3])
    except:
        pass
with open('paths.txt', 'w') as f:
    for path in paths:
        f.write(path)
        f.write('\n')