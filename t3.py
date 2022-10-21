import nltk
import re
import numpy as np
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

titles_re = '[A-Z][A-Z- ]+[A-Z]'

CG_chapters = {}
P_chapters = {}

def split_into_chapters(book):
    chapters = {}

    titles = re.findall(titles_re, book)
    for i in range(len(titles)):
        if i < len(titles) - 1:
            chapter = re.search(titles[i] + '[\S\s]+' + titles[i+1], book).group()
            chapter = re.sub(titles[i], '', chapter)
            chapter = re.sub(titles[i+1], '', chapter)
        else:
            chapter = re.search(titles[i] + '[\S\s]+', book).group()
            chapter = re.sub(titles[i], '', chapter)

        words_in_chapter = re.findall('[^\s^\d]+', chapter)
        chapter = ' '.join(words_in_chapter)
        chapters[titles[i]] = chapter
    
    return chapters

# def Tokenize(doc):
#     Stopwords = list(set(nltk.corpus.stopwords.words('english')))

with open('ChildsGarden.txt', 'r') as file:
    CG_book = file.read()

with open('TheProphet.txt', 'r') as file:
    P_book = file.read()

CG_chapters = split_into_chapters(CG_book)
print(CG_chapters['BED IN SUMMER'])

P_chapters = split_into_chapters(P_book)
print(P_chapters['ON LOVE'])