import nltk 
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.stem.snowball import SnowballStemmer
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd



def preproccessing(tokens,stem):

    WN_lemmatizer = WordNetLemmatizer()
 
    tokens = [token for token in tokens if token not in '.,:;<>\'s!?[]()`"\'--']  # removing punctuation, unwanted characters/markup 

    stopwords = nltk.corpus.stopwords.words('english')
    tokens = [w.lower() for w in tokens if w.lower() not in stopwords]   # removing stops words

    stemmer = SnowballStemmer("english")
    if stem ==1:
        tokens = [stemmer.stem(word) for word in tokens]            # stemming the words 
    

    tokens = [WN_lemmatizer.lemmatize(token, pos="v") for token in tokens]

    return tokens 



def histogramplot(distlist):

    df = pd.DataFrame(distlist, columns=['word', 'frequency'])

    df.plot(kind='bar', x='word', y='frequency',width=1)    #ploting the data
    plt.title("30 most frequent words in the Book")
    plt.ylabel("Frequency")
    plt.xlabel("Words")
    plt.savefig('frequencyplot.png')
    plt.show()
    


    writer = pd.ExcelWriter('python_plot.xlsx', engine = 'xlsxwriter')    #saving data into excel file 
    df.to_excel(writer, sheet_name='Sheet1', startrow=1, header=False)
    writer.save()

    print(distlist)                 #printing the list to terminal 

def poetryanalysis(Book):

    PreProccessedTokens = word_tokenize(Book)
    tokens= preproccessing(PreProccessedTokens,1)  # 1 means using stemming
    fdist = nltk.FreqDist(tokens)
    distlist=fdist.most_common(30)
    return distlist
    
def poetryanalysisWOstemming(Book):
    PreProccessedTokens = word_tokenize(Book)
    tokens= preproccessing(PreProccessedTokens,0)   # 0 means no stemming
    fdist = nltk.FreqDist(tokens)
    distlist=fdist.most_common(50)
    return distlist    






def main():
    TheProphet = "TheProphet.txt"
    ChildsGarden = "ChildsGarden.txt"


    f = open(ChildsGarden)
    Book = f.read()

    distlist= poetryanalysis(Book)
    histogramplot(distlist) 

if __name__ == "__main__":
    main()