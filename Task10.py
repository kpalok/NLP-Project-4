import re
import nltk
import numpy as np
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

titles_re = '.*[A-Z][A-Z- \']{2,}[A-Z?].*'

def read_poem_lines(book_filename):
    with open(book_filename, 'r') as file:
        # filter out titles and empty lines
        lines = [re.sub('\n', '', line).strip() for line in file.readlines() if re.match(titles_re, line) is None and re.match('^\s*$', line) is None]

    return lines

def calc_LD(lines):
    Stopwords = list(set(nltk.corpus.stopwords.words('english')))
    stemmer = SnowballStemmer("english")
    WN_lemmatizer = WordNetLemmatizer()
    lines_LD = []

    for line in lines:
        words = word_tokenize(line)
        # words = [stemmer.stem(word) for word in words]
        # words = [WN_lemmatizer.lemmatize(word, pos="v") for word in words]
        # words = [word for word in words if word.isalpha() and word not in Stopwords] #get rid of numbers and Stopwords
        words = nltk.pos_tag(words, tagset='universal')

        ADJ_and_ADV_count = len([word for (word, tag) in words if tag == 'ADJ' or tag == 'ADV'])
        VERB_count = len([word for (word, tag) in words if tag == 'VERB'])

        if VERB_count == 0:
            VERB_count = 1

        LD = float(ADJ_and_ADV_count) / float(VERB_count)

        lines_LD.append(LD)

    return np.array(lines_LD)

CG_lines = read_poem_lines('ChildsGarden.txt')
CG_LD = calc_LD(CG_lines)
np.savetxt('Task 10 Results/ChildsGarden_LD.csv', np.vstack((np.arange(len(CG_LD)), CG_LD)).T, delimiter=',')

P_lines = read_poem_lines('TheProphet.txt')
P_LD = calc_LD(P_lines)
np.savetxt('Task 10 Results/TheProphet_LD.csv', np.vstack((np.arange(len(P_LD)), P_LD)).T, delimiter=',')

fig, ax = plt.subplots(2, 1)
fig.suptitle('Lexical diversities for each line of the poem', fontsize=12)

ax[0].set_title('Childrens Garden of Verses', fontsize=8)
ax[0].bar(np.arange(len(CG_LD)), CG_LD)

ax[1].set_title('The Prophet', fontsize=8)
ax[1].bar(np.arange(len(P_LD)), P_LD)

plt.show()
