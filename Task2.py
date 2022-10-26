import nltk 
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
import numpy as np
import pandas as pd
import script
from fuzzywuzzy import fuzz
import re
from tabulate import tabulate

def fuzzyvariation(list,titles):
    elements=[]

    for i in range(len(list)):
        similarity=[]
        similarity.append(list[i])
        for x in range(len(titles)):
            
            similarity.append(fuzz.WRatio(list[i],titles[x]))
        elements.append(similarity)


    
      
    header=terminaltable(elements,titles)

    exporttoexcel(elements,header,'fuzzy') 

def terminaltable(elements,titles):
    
    header=['word','title']
    for i in range(1,len(titles)):
        header.append(i) 
 
    print(tabulate(elements, headers=header)) 
    print("the main book title: ",titles[0]," the", len(titles)-1, "chapters of the book: ",titles[1:])
    return header



def wupsimilarity(listwup,titles):

    elements=[]
    for i in range(len(listwup)):
        similarity=[]
        similarity.append(listwup[i])
        S1 = wn.synsets(listwup[i])[0]  #S1 for the word 
        for x in range(len(titles)):
            counter=0
            res=0.0
            words = word_tokenize(titles[x])     #we start by tokenizing each title  
            for word in words:                  #looping through each word in title 
                S2=wn.synsets(word)             #synset for each word
                if S2:                          #checking if the word exists in synset 
                    S2=wn.synsets(word)[0]      
                    score=S1.wup_similarity(S2)         #similarity between common word and the word in title 
                    res += score                        #adding similarity score 
                    counter +=1                         #counting the number of similarities
            if counter != 0:
                res= res/counter                        #final result would be the average of similarites of all word in title
            similarity.append(res)
        elements.append(similarity)

    header=terminaltable(elements,titles)
    exporttoexcel(elements,header,'wup') 



def exporttoexcel(elements,header,type):

    content=tabulate(elements, headers=header)
    if type == 'fuzzy':
        text_file=open("output_table_fuzzy.csv","w")
    else:
        text_file=open("output_table_wup.csv","w")
    text_file.write(content)
    text_file.close()    



def getcommonwords(distlist):
    list=[]
    for i in range(len(distlist)):
        list.append(distlist[i][0])   
    return list 

def gettitles(Book,maintitle):   
    titles_re = '[A-Z][A-Z- \']{2,}[A-Z?]'
    titles = re.findall(titles_re, Book)            #list of all chapter titles 
    titles.insert(0,maintitle)
    return titles


def processedwordnet(listwup):
    newlist=[]
    for i in range(len(listwup)):
        S1 = nltk.corpus.wordnet.synsets(listwup[i])
        if S1:
            newlist.append(listwup[i])

    return newlist

def main():
    TheProphet = "TheProphet.txt"
    ChildsGarden = "ChildsGarden.txt"
    maintitle='Childs Garden'

    f = open(ChildsGarden)
    Book = f.read()
    distlist= script.poetryanalysis(Book)
    

    list= getcommonwords(distlist)                #list of most common 30 words
    titles= gettitles(Book,maintitle) 
    fuzzyvariation(list,titles)


    distlistwup= script.poetryanalysisWOstemming(Book) #tokenizing the book without stemming because it affects the accuracy of word net
    listwup= getcommonwords(distlistwup)
    listwup= processedwordnet(listwup)   #we extracted the most common words that exist in word net dictionary 
    listwup=listwup[:30]              #we need the most common 30 words



    wupsimilarity(listwup,titles) 
    



if __name__ == "__main__":
    main()