#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import nltk
import numpy as np
import matplotlib.pyplot as plt
from nltk import word_tokenize
from nltk.corpus import sentiwordnet as swn
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer as lem
import pandas as pd
import math
from Task6 import prepare_book, preprocess_book, calc_sent_per_line, split_to_10_values

def histogram_plot(sent, book, chapter):
    pt = pd.DataFrame(sent, columns=['Negative sentiment'])
    pt.plot(kind='bar')
    if book == 'ChildsGarden.txt':
        if chapter == 'one':
            plt.title("Negative sentiment in chapter one of ChildsGarden book")
            plt.ylabel("Negative Sentiment")
            plt.xlabel("Chapter One")
            plt.savefig('NegativeSent_ChildsGarden_Chapterone.png')
        elif chapter == 'all':
            plt.title("Negative sentiment in ChildsGarden book")
            plt.ylabel("Sentiment")
            plt.xlabel("Book")
            plt.savefig('NegativeSent_ChildsGarden_book.png')

    elif book == 'TheProphet.txt':
        if chapter == 'one':
            plt.title("Negative sentiment in chapter one of TheProphet book")
            plt.ylabel("Negative Sentiment")
            plt.xlabel("Chapter One")
            plt.savefig('NegativeSent_TheProphet_Chapterone.png')
        elif chapter == 'all':
            plt.title("Negative sentiment in TheProphet book")
            plt.ylabel("Sentiment")
            plt.xlabel("Book")
            plt.savefig('NegativeSent_TheProphet_book.png')
    plt.show()
############ TheProphet book, whole book analysis ###################
file_TheProphet = open('TheProphet.txt', encoding="utf8")
Lines = file_TheProphet.readlines()
book_without_index, first_chapter = prepare_book(Lines)
preprocessd_book = preprocess_book(book_without_index)
sentiment_per_line = calc_sent_per_line(preprocessd_book, 'neg')
sentiment_10_values = split_to_10_values(sentiment_per_line)
histogram_plot(sentiment_10_values, file_TheProphet.name, 'all')
############ TheProphet book, first chapter analysis ###################
preprocessd_book = preprocess_book(first_chapter)
sentiment_per_line = calc_sent_per_line(preprocessd_book, 'neg')
sentiment_10_values = split_to_10_values(sentiment_per_line)
histogram_plot(sentiment_10_values, file_TheProphet.name, 'one')

############ ChildsGarden book, whole book analysis ###################
file_ChildsGarden = open('ChildsGarden.txt', encoding="utf8")
Lines = file_ChildsGarden.readlines()
book_without_index, first_chapter = prepare_book(Lines)
preprocessd_book = preprocess_book(book_without_index)
sentiment_per_line = calc_sent_per_line(preprocessd_book, 'neg')
sentiment_10_values = split_to_10_values(sentiment_per_line)
histogram_plot(sentiment_10_values, file_ChildsGarden.name, 'all')

############ ChildsGarden book, first chapter analysis ###################
preprocessd_book = preprocess_book(first_chapter)
sentiment_per_line = calc_sent_per_line(preprocessd_book, 'neg')
sentiment_10_values = split_to_10_values(sentiment_per_line)
histogram_plot(sentiment_10_values, file_ChildsGarden.name, 'one')