import pandas as pd
import numpy as np
import sys
import os
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import precision_recall_fscore_support


import warnings
warnings.filterwarnings("ignore")

def word_sum(text):
    words = text.replace('.,/?><;:\'\"\\|][}\{\}1234567890!@#$%^&*()-=_+`~]', '').split(' ')
    summation = 0
    for word in words:
        summation += len(word)
    return summation

def main():
    N = 100
    f = sys.argv[1]
    df = None
    try:
        df = pd.read_csv(f, sep='\t')
    except:
        df = pd.read_csv(f, sep='\t', encoding='ISO-8859-1')
    df = df[['pid', 'text']]
    df['num_words'] = df.text.apply(lambda x: len(x.split(' ')))
    speaker_words = df.groupby('pid')['num_words'].aggregate("sum")
    top_speakers = speaker_words.sort_values(ascending=False)[:N]
    top_speakerid = list(top_speakers.index)
    df = df[df['pid'].isin(top_speakerid)]

    df_word_len = df.text.apply(word_sum)
    df_avg_word = df_word_len/df['num_words']

    # COUNTS OF ADJ AND ADVERBS
    #JJ, JJR, JJS, RB, RBR, RBS, UH
    adj_pos = ['JJ', 'JJR', 'JJS']
    adv_pos = ['RB', 'RBR', 'RBS']
    uh_pos = ['UH']
    adj_counts = []
    adv_counts = []
    uh_counts = []
    for t in df.text:
        adj = 0
        adv = 0
        uh = 0
        tags = nltk.pos_tag(nltk.word_tokenize(t))
        for tag in tags:
            if tag[1] in adj_pos:
                adj += 1
            elif tag[1] in adv_pos:
                adv += 1
            elif tag[1] in uh_pos:
                uh += 1
        adj_counts.append(adj)
        adv_counts.append(adv)
        uh_counts.append(uh)

    # TF-IDF vectorizor
    vec = TfidfVectorizer(norm=None, stop_words={"english"})
    vec.fit(df["text"])
    tf_idf_sparse = vec.transform(df["text"])
    texts = pd.DataFrame(tf_idf_sparse.todense())
    texts.columns = vec.vocabulary_

    #ADDING FEATURES
    texts['df_avg_word'] = list(df_avg_word)
    texts['adj_counts'] = adj_counts
    texts['adv_counts'] = adv_counts
    texts['uh_counts'] = uh_counts

    X = texts
    y = df.pid
    X = X.rename(columns = {'fit' : 'fit_feature'})
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = .25, random_state=1)

    scaler = StandardScaler()
    scaler.fit(X_train)
    X_train_sc = scaler.transform(X_train)
    X_test_sc = scaler.transform(X_test)

    # GRID SEARCH
    # print("RUNNING GRID SEARCH:::::::::::::::::::::::::::::::::")
    # param_grid = {'solver':['lbfgs', 'sgd', 'adam'],
    #  'alpha':[1e-5],
    #   'hidden_layer_sizes':[(9, 3), (8, 3), (7, 3), (7, 4)], 'random_state':[1]}
    # grid = GridSearchCV(MLPClassifier(), param_grid, cv=3, iid=False)
    # grid.fit(X_test_sc, y_test)
    # model = grid.best_estimator_
    # print(model)

    highest_count = str(y_test.value_counts().sort_values(ascending=False).index[0])

    clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(7, 3), random_state=1)
    clf.fit(X_train_sc, y_train)

    y_pred = clf.predict(X_test_sc)

    stuff = precision_recall_fscore_support(y_test,y_pred,average='weighted')
    print("ACCURACY/PRECISION: ", stuff[0])
    print("RECALL: ", stuff[1])
    print("F1-SCORE: ", stuff[2])

if __name__=="__main__":
     main()
