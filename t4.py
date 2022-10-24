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
    pos_token_lengths = {
        "ADJ": np.array([]),
        "ADP": np.array([]),
        "ADV": np.array([]),
        "CONJ": np.array([]),
        "DET": np.array([]),
        "NOUN": np.array([]),
        "NUM": np.array([]),
        "PRT": np.array([]),
        "PRON": np.array([]),
        "VERB": np.array([]),
        ".": np.array([]),
        "X": np.array([])
    }

    for sentence in sentences:
        words = word_tokenize(sentence)
        words = nltk.pos_tag(words, tagset='universal')
        words = [(stemmer.stem(word), tag) for (word, tag) in words]
        words = [(WN_lemmatizer.lemmatize(word, pos="v"), tag) for (word, tag) in words]
        words = [(word, tag) for (word, tag) in words if word.isalpha() and word not in Stopwords] #get rid of numbers and Stopwords

        for token, tag in words:
            pos_token_lengths[tag] = np.append(pos_token_lengths[tag], len(token))

    return pos_token_lengths

def plot_POS_token_length_histograms(book_name, chapters):
    cross_chapter_pos_token_lengths = {
        "ADJ": np.array([]),
        "ADP": np.array([]),
        "ADV": np.array([]),
        "CONJ": np.array([]),
        "DET": np.array([]),
        "NOUN": np.array([]),
        "NUM": np.array([]),
        "PRT": np.array([]),
        "PRON": np.array([]),
        "VERB": np.array([]),
        ".": np.array([]),
        "X": np.array([])
    }

    for j, title in enumerate(chapters):
        pos_token_lengths = get_token_lengths_by_POS_tag(chapters[title])

        fig, ax = plt.subplots(3, 4)
        fig.suptitle(book_name + ' chapter ' + title + ' token lengths per POS tag', fontsize=12)

        row = 0
        for i, tag in enumerate(pos_token_lengths):
            token_lengths = pos_token_lengths[tag]

            cross_chapter_pos_token_lengths[tag] = np.concatenate((cross_chapter_pos_token_lengths[tag], token_lengths))

            # Draw histogram only for cross chapter summary, save chapter-wise figures to image folder.
            # not very readable to display ~100 figures
            if i - 4 * row == 4:
                row = row + 1
            
            i = i - 4 * row
            # histogram discretization
            if (len(token_lengths) > 0):
                d = 1
                left_of_first_bin = token_lengths.min() - float(d)/2
                right_of_last_bin = token_lengths.max() + float(d)/2

                ax[row, i].hist(token_lengths, np.arange(left_of_first_bin, right_of_last_bin + d, d))
            else:
                ax[row, i].hist(token_lengths)

            ax[row, i].set_title(tag, fontsize=8)
            ax[row, i].set_xticks(np.unique(token_lengths))
            
        plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.90, wspace=0.20, hspace=0.60)
        fig.savefig('./Task 4 Histograms/' + book_name + '/' + re.sub('[!@#$?\']', '', title) + '.jpg')
        plt.close(fig)

    fig, ax = plt.subplots(3, 4)
    fig.suptitle(book_name + ' cross chapter token lengths per POS tag', fontsize=12)

    row = 0
    for i, tag in enumerate(cross_chapter_pos_token_lengths):
        if i - 4 * row == 4:
            row = row + 1
        
        i = i - 4 * row

        token_lengths = cross_chapter_pos_token_lengths[tag]

        # histogram discretization
        if (len(token_lengths) > 0):
            d = 1
            left_of_first_bin = token_lengths.min() - float(d)/2
            right_of_last_bin = token_lengths.max() + float(d)/2

            ax[row, i].hist(token_lengths, np.arange(left_of_first_bin, right_of_last_bin + d, d))
        else:
            ax[row, i].hist(token_lengths)

        ax[row, i].set_title(tag, fontsize=8)
        ax[row, i].set_xticks(np.unique(token_lengths))

    plt.subplots_adjust(left=0.05, bottom=0.05, right=0.95, top=0.90, wspace=0.20, hspace=0.60)

with open('ChildsGarden.txt', 'r') as file:
    CG_book = file.read()

with open('TheProphet.txt', 'r') as file:
    P_book = file.read()

# childs garden 64 chapters
CG_chapters = split_into_chapters(CG_book)
# the prophet 28 chapters
P_chapters = split_into_chapters(P_book)

plot_POS_token_length_histograms('Childrens Garden of Verses', CG_chapters)
plot_POS_token_length_histograms('The Prophet', P_chapters)

plt.show()