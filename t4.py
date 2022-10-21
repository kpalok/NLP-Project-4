import re
import nltk
import numpy as np
import matplotlib.pyplot as plt
from t3 import split_into_chapters
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

# Same function from task 3 but with part-of-speech tokens
def get_token_lengths_by_POS_tag(chapter):
    Stopwords = list(set(nltk.corpus.stopwords.words('english')))
    stemmer = SnowballStemmer("english")
    WN_lemmatizer = WordNetLemmatizer()

    sentences = sent_tokenize(chapter)
    # token length per POS tag in chapter
    pos_token_lengths = {}
    for sentence in sentences:
        words = word_tokenize(sentence)
        words = nltk.pos_tag(words, tagset='universal')
        words = [(stemmer.stem(word), tag) for (word, tag) in words]
        words = [(WN_lemmatizer.lemmatize(word, pos="v"), tag) for (word, tag) in words]
        words = [(word, tag) for (word, tag) in words if word.isalpha() and word not in Stopwords] #get rid of numbers and Stopwords

        for token, tag in words:
            if tag in pos_token_lengths:
                pos_token_lengths[tag] = np.append(pos_token_lengths[tag], token)
            else:
                pos_token_lengths[tag] = np.array([token])
    print(pos_token_lengths)
    return pos_token_lengths

with open('ChildsGarden.txt', 'r') as file:
    CG_book = file.read()

with open('TheProphet.txt', 'r') as file:
    P_book = file.read()

# childs garden 64 chapters
CG_chapters = split_into_chapters(CG_book)
# the prophet 28 chapters
P_chapters = split_into_chapters(P_book)


get_token_lengths_by_POS_tag(CG_chapters["BED IN SUMMER"])
