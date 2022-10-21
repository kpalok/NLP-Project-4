import nltk
import re
import numpy as np
import matplotlib.pyplot as plt
from nltk.tokenize import sent_tokenize, word_tokenize

titles_re = '[A-Z][A-Z- \']{2,}[A-Z?]'

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

def get_word_lengths(chapter):
    Stopwords = list(set(nltk.corpus.stopwords.words('english')))

    sentences = sent_tokenize(chapter)
    token_lengths = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        word_lengths = [len(word) for word in words if word.isalpha() and word not in Stopwords] #get rid of numbers and Stopwords

        token_lengths.extend(word_lengths)

    return np.array(token_lengths)

def plot_token_length_histograms(book_name, chapters, nrows, ncolumns):
    fig, ax = plt.subplots(nrows, ncolumns)
    fig.canvas.set_window_title(book_name + ' token lengths per chapter')
    fig.suptitle(book_name + ' token lengths per chapter', fontsize=12)
    row = 0
    cross_chapter_word_lengths = []
    for i, title in enumerate(chapters):
        if i - ncolumns * row == ncolumns:
            row = row + 1
        
        i = i - ncolumns * row
        word_lengths = get_word_lengths(chapters[title])
        cross_chapter_word_lengths.extend(word_lengths)

        # histogram discretization from https://stackoverflow.com/questions/30112420/histogram-for-discrete-values-with-matplotlib
        d = np.diff(np.unique(word_lengths)).min()
        left_of_first_bin = word_lengths.min() - float(d)/2
        right_of_last_bin = word_lengths.max() + float(d)/2

        ax[row, i].hist(word_lengths, np.arange(left_of_first_bin, right_of_last_bin + d, d))
        ax[row, i].set_title(title, fontsize=8)
        ax[row, i].set_xticks(np.unique(word_lengths))

    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.90, wspace=0.20, hspace=0.60)

    fig = plt.figure(book_name + ' token lengths cross-chapter')
    fig.suptitle(book_name + ' token lengths cross-chapter', fontsize=12)

    cross_chapter_word_lengths = np.array(cross_chapter_word_lengths)

    d = np.diff(np.unique(cross_chapter_word_lengths)).min()
    left_of_first_bin = cross_chapter_word_lengths.min() - float(d)/2
    right_of_last_bin = cross_chapter_word_lengths.max() + float(d)/2

    plt.hist(cross_chapter_word_lengths, np.arange(left_of_first_bin, right_of_last_bin + d, d))
    plt.xticks(np.unique(cross_chapter_word_lengths))

with open('ChildsGarden.txt', 'r') as file:
    CG_book = file.read() 

with open('TheProphet.txt', 'r') as file:
    P_book = file.read()

# childs garden 64 chapters
CG_chapters = split_into_chapters(CG_book)
# the prophet 28 chapters
P_chapters = split_into_chapters(P_book)

plot_token_length_histograms('Childrens Garden of Verses', CG_chapters, 8, 8)

plot_token_length_histograms('The Prophet', P_chapters, 7, 4)

plt.show()