import nltk 
from nltk.tokenize import word_tokenize
import Task1
import jellyfish
import fuzzywuzzy
import phonetics
from difflib import SequenceMatcher
import re
from tabulate import tabulate
import pandas as pd
import matplotlib.pyplot as plt




titles_re = '.*[A-Z][A-Z- \']{2,}[A-Z?].*'

def read_poem_lines(book_filename):
    with open(book_filename, 'r') as file:
        # filter out titles and empty lines
        lines = [re.sub('\n', '', line).strip() for line in file.readlines() if re.match(titles_re, line) is None and re.match('^\s*$', line) is None]

    return lines

def dataplot(elements):

    df = pd.DataFrame(elements[:40], columns=['line', 'similarity'])   #working on the first 40 lines samlpe for visualizing to gain better insights

    df.plot(kind='scatter', x='line', y='similarity')    #ploting the data
    plt.title("phonetic similarity between first and last word in each line")
    plt.ylabel("phonetic similarity")
    plt.xlabel("lines")
    plt.savefig('phonetic similarity plot.png')
    plt.show()
    


def gettwowords(line):
    tokens=word_tokenize(line)
    tokens = [token for token in tokens if token not in '.,:;<>\'s!?[]()`"\'--``_']  # removing punctuation, unwanted characters/markup
    words=[]
    words.append(tokens[0])
    words.append(tokens[len(tokens)-1])
    return words

def getlcs(phowords):
    seqMatch = SequenceMatcher(None,phowords[0],phowords[1])
    match = seqMatch.find_longest_match(0, len(phowords[0]), 0, len(phowords[1]))
    lcs=phowords[0][match.a: match.a + match.size]   #calculating longest common substring
    return lcs

def findsimilarity(words):
    phowords=[]
    phowords.append(phonetics.metaphone(words[0]))
    phowords.append(phonetics.metaphone(words[1]))
    lcs= getlcs(phowords)
    if len(phowords[0])+len(phowords[1]) ==0:
        return 0
    else:
        sim=(2*len(lcs)/(len(phowords[0])+len(phowords[1])))
        return round(sim,3) 

def similarities(lines):
    
    elements=[]
    count=1
    for line in lines:
        sim=[]
        sim.append(count) 
        words=gettwowords(line)
        sim.append(findsimilarity(words))
        count += 1
        elements.append(sim)
    exporttoexcel(elements)
    dataplot(elements)
    


def exporttoexcel(elements):
    header=['line','phonetic similarity']  
    content=tabulate(elements, headers=header)
    text_file=open("output_table_phonetic_similarity.csv","w")
    text_file.write(content)
    text_file.close()    


def main():
    


    TheProphet = "TheProphet.txt"
    ChildsGarden = "ChildsGarden.txt"


    lines = read_poem_lines(ChildsGarden)
    similarities(lines)



    

if __name__ == "__main__":
    main()
