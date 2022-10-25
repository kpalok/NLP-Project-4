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

document = open("TheProphet.txt", 'r') #, encoding="utf8"
for i in range(1): #hack: skip first x lines
    next(document)
prophet = getChapters(document, 65)
document.close()

#calculate empath weights per line. done in bigram style: 1-2,2-3,3-4...
from empath import Empath
lexicon = Empath()
from sklearn.metrics.pairwise import cosine_similarity

garden_empath = []
for i in range(len(garden)):
    temp = []
    for j in range(len(garden[i])):
        if(j+1<len(garden[i])):
            a = lexicon.analyze(garden[i][j], normalize=True)
            a_val = [list(a.values())]
            b = lexicon.analyze(garden[i][j+1], normalize=True)
            b_val = [list(b.values())]
            temp.append(cosine_similarity(a_val,b_val)[0][0])
    garden_empath.append(temp)
print(garden_empath)

prophet_empath = []
for i in range(len(prophet)):
    temp = []
    for j in range(len(prophet[i])):
        if(j+1<len(prophet[i])):
            a = lexicon.analyze(prophet[i][j], normalize=True)
            a_val = [list(a.values())]
            b = lexicon.analyze(prophet[i][j+1], normalize=True)
            b_val = [list(b.values())]
            temp.append(cosine_similarity(a_val,b_val)[0][0])
    prophet_empath.append(temp)
print(prophet_empath)


#graph scores by chapter
import numpy as np
import matplotlib.pyplot as plt

garden_var = [] #save variance per chapter for plotting
for i in range(len(garden_empath)):
    y=np.var(garden_empath[i])
    garden_var.append(y)

prophet_var = []
for i in range(len(prophet_empath)):
    y=np.var(prophet_empath[i])
    prophet_var.append(y)


plt.figure(figsize=(14,6))
plt.plot(np.arange(1,len(garden_var)+1), garden_var, label = "Garden")
plt.xlabel('chapter')
plt.ylabel('variance in empath scores')
plt.legend()
plt.savefig("Garden_empath.png")
plt.show()

plt.figure(figsize=(14,6))
plt.plot(np.arange(1,len(prophet_var)+1),prophet_var, label = "Prophet")
plt.xlabel('chapter')
plt.ylabel('variance in empath scores')
plt.legend()
plt.savefig("Prophet_empath.png")
plt.show()