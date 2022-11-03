import nltk
import re
import numpy as np
import matplotlib.pyplot as plt
from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

titles_re = '[A-Z][A-Z- \']{2,}[A-Z?]'

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
        chapter = ' '.join(words_in_chapter).lower()
        chapters[titles[i]] = chapter
    
    return chapters

def get_token_lengths(chapter):
    Stopwords = list(set(nltk.corpus.stopwords.words('english')))
    stemmer = SnowballStemmer("english")
    WN_lemmatizer = WordNetLemmatizer()

    sentences = sent_tokenize(chapter)
    token_lengths = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        words = [stemmer.stem(word) for word in words]
        words = [WN_lemmatizer.lemmatize(word, pos="v") for word in words]

        sentence_token_lengths = [len(word) for word in words if word.isalpha() and word not in Stopwords] #get rid of numbers and Stopwords

        token_lengths.extend(sentence_token_lengths)

    return np.array(token_lengths)

def plot_token_length_histograms(book_name, chapters, nrows, ncolumns):
    fig, ax = plt.subplots(nrows, ncolumns)
    fig.suptitle(book_name + ' token lengths per chapter', fontsize=12)
    row = 0
    cross_chapter_token_lengths = []
    for i, title in enumerate(chapters):
        if i - ncolumns * row == ncolumns:
            row = row + 1
        
        i = i - ncolumns * row
        token_lengths = get_token_lengths(chapters[title])
        cross_chapter_token_lengths.extend(token_lengths)

        # histogram discretization from https://stackoverflow.com/questions/30112420/histogram-for-discrete-values-with-matplotlib
        d = 1
        left_of_first_bin = token_lengths.min() - float(d)/2
        right_of_last_bin = token_lengths.max() + float(d)/2

        ax[row, i].hist(token_lengths, np.arange(left_of_first_bin, right_of_last_bin + d, d))
        ax[row, i].set_title(title, fontsize=8)
        ax[row, i].set_xticks(np.unique(token_lengths))

    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.99, top=0.90, wspace=0.20, hspace=0.60)

    fig = plt.figure(book_name + ' token lengths cross-chapter')
    fig.suptitle(book_name + ' token lengths cross-chapter', fontsize=12)

    cross_chapter_token_lengths = np.array(cross_chapter_token_lengths)

    d = np.diff(np.unique(cross_chapter_token_lengths)).min()
    left_of_first_bin = cross_chapter_token_lengths.min() - float(d)/2
    right_of_last_bin = cross_chapter_token_lengths.max() + float(d)/2

    plt.hist(cross_chapter_token_lengths, np.arange(left_of_first_bin, right_of_last_bin + d, d))
    plt.xticks(np.unique(cross_chapter_token_lengths))
    plt.xlabel('Token length')
    plt.ylabel('Count')

if __name__ == "__main__":
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