import re #regexp for string editing

def getChapters(document, amountOfChap): #function for reading a certain amount of chapters from the book, saved to a 2d list
    numOfChaps = 0
    chapsWanted = amountOfChap
    chap = []
    linesByChap = []
    newChap = False

    while True:
        line = document.readline()

        if(len(line)==0): #if EOF
            break
        if(line.isupper()): #if the line is all-uppercase, it begins a new chapter
            numOfChaps+=1
            newChap = True
        if(numOfChaps>chapsWanted): #if number of chapters exceed amount wanted, break loop
            break

        print(line)

        #do editing to remove spaces, line breaks, empty lines, extra lines added by gutenberg
        line = line.strip() #remove leading and trailing whitespaces
        line = re.sub(r'[^a-zA-Z\'_ ]+', '', line) #use regex to remove non-letter non-space characters
        if(line.strip()==''): #if line is empty after editing, skip
            continue
        line = line.lower() #set line to lowercase letters only


        if(newChap == False): #append each line to temporary array
            chap.append(line)
        elif(newChap == True): #if chapter has ended, append temporary array to return array
            print("New chapter: "+line)
            newChap = False
            linesByChap.append(chap)
            chap = []

    return linesByChap #return 2d list of [chapter number][chapter by line]


document = open("ChildsGarden.txt", 'r')
for i in range(1): #hack: skip first x lines
    next(document)
garden = getChapters(document, 65)
document.close()
print(garden[0])

# find named-entities with spacy
import spacy
spc = spacy.load("en_core_web_sm")
import numpy as np
import pandas as pd

entsByChap = []
for i in range(len(garden)): #chapters
    string = ' '.join(garden[i]) #spacy requires a string as input. join the lines of entire chapter together into a single string
    doc = spc(string)
    temp = []
    for ent in doc.ents:
        print(ent.text+":"+ent.label_)
        temp.append(ent.label_) #append labels to array
    entsByChap.append(temp) #ordered by chapter

print(entsByChap)

unique_labels = np.unique(np.concatenate((pd.Index(entsByChap)).values)) #get all unique labels in book
#print(unique_labels[0])


labels_sorted = []
labels_sorted_df = pd.DataFrame({})
for i in range(len(unique_labels)):
    labels_sorted_df[unique_labels[i]] = ""
for i in range(len(entsByChap)):
    labels_sorted_df = labels_sorted_df.append(pd.Series(), ignore_index = True)
print(labels_sorted_df)


for i in range(len(entsByChap)):
    labels_index = pd.Index(entsByChap[i]) #turn labels array into pandas index for label/count
    print(labels_index)
    for j in range(len(labels_index.value_counts())):
        labels_sorted_df.loc[i,labels_index.value_counts().index[j]]=[labels_index.value_counts()[j]]
print(labels_sorted_df) #label counts in a single pandas dataframe. this allows for easier graphing by columns

#calculate standard deviation and mean for labels across chapters
print("GARDEN MEAN")
print(labels_sorted_df.mean())
print("GARDEN STANDARD DEVIATION")
print(labels_sorted_df.std())

#graph results by chapter
import matplotlib.pyplot as plt
count=len(unique_labels)
for i in range(len(unique_labels)):
    indexes = labels_sorted_df.loc[:,unique_labels[i]]
    indexes.fillna(0)
    plt.figure()
    plt.locator_params(integer=True)
    indexes.plot.bar(title="Garden: "+unique_labels[i],xlabel='chapter',ylabel='count',figsize=(14,6))
    plt.savefig("Garden_"+unique_labels[i]+".png")
    
    plt.show()

###########
###########
#simply copypasted the code for garden here, to be used for prophet. not pretty, but functional
###########
###########
document = open("TheProphet.txt", 'r')
for i in range(1): #hack: skip first x lines
    next(document)
garden = getChapters(document, 65)
document.close()
print(garden[0])

# find named-entities with spacy
"""import spacy
spc = spacy.load("en_core_web_sm")
import numpy as np
import pandas as pd"""

entsByChap = []
for i in range(len(garden)): #chapters
    string = ' '.join(garden[i]) #spacy requires a string as input. join the lines of entire chapter together into a single string
    doc = spc(string)
    temp = []
    for ent in doc.ents:
        print(ent.text+":"+ent.label_)
        temp.append(ent.label_) #append labels to array
    entsByChap.append(temp) #ordered by chapter

print(entsByChap)

unique_labels = np.unique(np.concatenate((pd.Index(entsByChap)).values)) #get all unique labels in book
#print(unique_labels[0])


labels_sorted = []
labels_sorted_df = pd.DataFrame({})
for i in range(len(unique_labels)):
    labels_sorted_df[unique_labels[i]] = ""
for i in range(len(entsByChap)):
    labels_sorted_df = labels_sorted_df.append(pd.Series(), ignore_index = True)
print(labels_sorted_df)


for i in range(len(entsByChap)):
    labels_index = pd.Index(entsByChap[i]) #turn labels array into pandas index for label/count
    print(labels_index)
    for j in range(len(labels_index.value_counts())):
        labels_sorted_df.loc[i,labels_index.value_counts().index[j]]=[labels_index.value_counts()[j]]
print(labels_sorted_df) #label counts in a single pandas dataframe. this allows for easier graphing by columns

#calculate standard deviation and mean for labels across chapters
print("PROPHET MEAN")
print(labels_sorted_df.mean())
print("PROPHET STANDARD DEVIATION")
print(labels_sorted_df.std())

#graph results by chapter
import matplotlib.pyplot as plt
count=len(unique_labels)
for i in range(len(unique_labels)):
    indexes = labels_sorted_df.loc[:,unique_labels[i]]
    indexes.fillna(0)
    plt.figure()
    plt.locator_params(integer=True)
    indexes.plot.bar(title="Prophet: "+unique_labels[i],xlabel='chapter',ylabel='count',figsize=(14,6))
    plt.savefig("Prophet_"+unique_labels[i]+".png")
    plt.show()