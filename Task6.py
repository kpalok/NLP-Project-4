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

def rem_EmptyLines_EOL(book):
    preprocessed_book = []
    for line in book:
        found = re.search('\n', line)  # remove \n at the end of each line
        if found is not None:
            line = re.sub(found.group(), '', line)  # remove empty lines
        if not re.match(r'^\s*$', line):
            preprocessed_book.append(line)
    return preprocessed_book

def Get_First_Chapter(book):
    chapters_count=0
    first_chapter = []
    for line in book:
        if re.search('[A-Z][A-Z- \']{2,}', line) is not None:
            if chapters_count == 2:
                break
            else:
                chapters_count += 1
        else:
            first_chapter.append(line)

    return first_chapter

def Remove_Chapters(book):
    book_without_chapters = []
    for line in book:
        if re.search('[A-Z][A-Z- \']{2,}', line) is None:
            book_without_chapters.append(line)
    return book_without_chapters

def prepare_book(book):
    book_without_lines = rem_EmptyLines_EOL(book)
    first_chapter = Get_First_Chapter(book_without_lines)
    book_without_index = Remove_Chapters(book_without_lines)
    return book_without_index, first_chapter

def preprocess_book(book):
    tokenized_book = []
    stopwords = nltk.corpus.stopwords.words('english')
    stemmer = SnowballStemmer("english")
    for line in book:
        tokenized_line = word_tokenize(line)  # tokenize each line
        tokenized_low_line = [token.lower() for token in tokenized_line if not re.match('[^\w\s]',
                                                                                        token)]  # change to lower case, remove special characters and stopwords
        if len(tokenized_low_line) != 0:
            tokenized_book.append([stemmer.stem(token) for token in tokenized_low_line if
                               token not in stopwords])  # Remove stopwords and apply stemming
    return tokenized_book


def word_sentiment(word, pos, sentiment):
    emotion = 0.0
    word_synts = swn.senti_synsets(word)
    word_synts = list(word_synts)
    for each in word_synts:
        if pos == each.synset._pos:
            if sentiment == 'pos':
                emotion += each.pos_score()
            else:
                emotion += each.neg_score()
    emotion = emotion / len(word_synts)
    return emotion


def calc_sent_per_line(book, sentiment):
    undefined_words = 0
    average_sentiment = []
    for line in book:
        if len(line) !=0:
            tagged_word = nltk.pos_tag(line)                                                                #Get tags of each word
            tagged_list = [(word, nltk.map_tag('en-ptb', 'universal', tag)) for word, tag in tagged_word]   #make a list of words and tags
            line_sentiment = 0.0
            for word, tag in tagged_list:
                if (tag == 'NOUN'):
                    tag = 'n'
                elif (tag == 'VERB'):
                    tag = 'v'
                elif (tag == 'ADJ'):
                    tag = 'a'
                elif (tag == 'ADV'):
                    tag = 'r'
                else:
                    tag = 'x'
                if (tag != 'x'):
                    try:
                        line_sentiment += word_sentiment(word, tag, sentiment)                          #Calculate sentiment for the word
                    except:
                        wor = lem.lemmatize(word, tag)                                                  #If word is not found, try lemmatization first
                        try:
                            line_sentiment += word_sentiment(wor, tag, sentiment)                       #Try again after lemmatization
                        except:
                            undefined_words += 1                                                        #Number of undefined word, used for debugging
            average_sentiment.append(line_sentiment / len(line))
    return average_sentiment

def split_to_10_values(values):
    ten_values = []
    total_value = 0.0
    median = math.floor(len(values)/10)
    cnt = 1
    for index in range(len(values)):
        total_value += values[index]
        if index >= median*cnt:
            cnt += 1
            ten_values.append(total_value/median)
            total_value = 0
            if cnt == 11:
                break
    return ten_values

def histogram_plot(data, book_name, chapter):
    pt = pd.DataFrame(data, columns=['Positive sentiment'])
    pt.plot(kind='bar')
    if book_name == 'ChildsGarden.txt':
        if chapter == 'one':
            plt.title("Positive sentiment in chapter one of ChildsGarden book")
            plt.ylabel("Positive Sentiment")
            plt.xlabel("Chapter One")
            plt.savefig('PositiveSent_ChildsGarden_Chapterone.png')
        elif chapter == 'all':
            plt.title("Positive sentiment in ChildsGarden book")
            plt.ylabel("Sentiment")
            plt.xlabel("Book")
            plt.savefig('PositiveSent_ChildsGarden_book.png')

    elif book_name == 'TheProphet.txt':
        if chapter == 'one':
            plt.title("Positive sentiment in chapter one of TheProphet book")
            plt.ylabel("Positive Sentiment")
            plt.xlabel("Chapter One")
            plt.savefig('PositiveSent_TheProphet_Chapterone.png')
        elif chapter == 'all':
            plt.title("Positive sentiment in TheProphet book")
            plt.ylabel("Sentiment")
            plt.xlabel("Book")
            plt.savefig('PositiveSent_TheProphet_book.png')
    plt.show()


############ TheProphet book, whole book analysis ###################
file_TheProphet = open('TheProphet.txt', encoding="utf8")
Lines = file_TheProphet.readlines()
book_without_index, first_chapter = prepare_book(Lines)
preprocessd_book = preprocess_book(book_without_index)
sentiment_per_line = calc_sent_per_line(preprocessd_book, 'pos')
sentiment_10_values = split_to_10_values(sentiment_per_line)
histogram_plot(sentiment_10_values, file_TheProphet.name, 'all')
############ TheProphet book, first chapter analysis ###################
preprocessd_book = preprocess_book(first_chapter)
sentiment_per_line = calc_sent_per_line(preprocessd_book, 'pos')
sentiment_10_values = split_to_10_values(sentiment_per_line)
histogram_plot(sentiment_10_values, file_TheProphet.name, 'one')

############ ChildsGarden book, whole book analysis ###################
file_ChildsGarden = open('ChildsGarden.txt', encoding="utf8")
Lines = file_ChildsGarden.readlines()
book_without_index, first_chapter = prepare_book(Lines)
preprocessd_book = preprocess_book(book_without_index)
sentiment_per_line = calc_sent_per_line(preprocessd_book, 'pos')
sentiment_10_values = split_to_10_values(sentiment_per_line)
histogram_plot(sentiment_10_values, file_ChildsGarden.name, 'all')

############ ChildsGarden book, first chapter analysis ###################
preprocessd_book = preprocess_book(first_chapter)
sentiment_per_line = calc_sent_per_line(preprocessd_book, 'pos')
sentiment_10_values = split_to_10_values(sentiment_per_line)
histogram_plot(sentiment_10_values, file_ChildsGarden.name, 'one')