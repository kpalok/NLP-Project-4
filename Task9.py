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

def dataplot(elements,name):

    df = pd.DataFrame(elements[:100], columns=['line', 'similarity'])   #working on the first 100 lines samlpe for visualizing to gain better insights

    df.plot(kind='scatter', x='line', y='similarity')    #ploting the data
    plt.title("phonetic similarity between first and last word for " + name + " book")
    plt.ylabel("phonetic similarity")
    plt.xlabel("lines")
    plotname = "scatter plot of phonetic similarity of %s book.png" %name
    plt.savefig(plotname)
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

def similarities(lines,name):
    
    elements=[]
    count=1
    for line in lines:
        sim=[]
        sim.append(count) 
        words=gettwowords(line)
        sim.append(findsimilarity(words))
        count += 1
        elements.append(sim)
    exporttoexcel(elements,name)
    dataplot(elements,name)
    


def exporttoexcel(elements,name):
    header=['line','phonetic similarity']  
    content=tabulate(elements, headers=header)
    filename="output table of phonetic similarity of %s book.csv" %name 
    text_file=open(filename,"w")
    text_file.write(content)
    text_file.close()    


def main():
    


    TheProphet = "TheProphet"
    ChildsGarden = "ChildsGarden"


    lines = read_poem_lines(TheProphet +".txt")
    similarities(lines,TheProphet)

    lines = read_poem_lines(ChildsGarden +".txt")
    similarities(lines,ChildsGarden)



    

if __name__ == "__main__":
    main()
