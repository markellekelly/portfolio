import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.metrics import precision_recall_fscore_support
from nltk.corpus import stopwords
from sklearn import tree
from sklearn import svm
from sklearn.decomposition import PCA
from sklearn.ensemble import BaggingClassifier,AdaBoostClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
import pickle

# random_state=1

def scorer(scores):
    ours = np.array(scores[1])
    # others = [scores[0]]
    # others.extend(scores[2:])
    # others = np.array(others)
    # a = others.mean()
    b = ours.mean()
    #score = 0.4*a + 0.6*b
    return b

def main():
    fin = open("question_tables.txt", 'r')
    team_id = []
    question = []
    answer = []
    topic = []
    for line in fin:
        attributes = line.split("|")
        if attributes[0] != "D1":
            team_id.append(attributes[0])
            question.append(attributes[1].replace("\n", ""))
            answer.append(attributes[2].replace("\n", ""))
            topic.append(attributes[3].replace(" \n", ""))
    fin.close()
    df = pd.DataFrame({"team_id":team_id, "question":question, "answer":answer, "topic":topic})
    df2 = df[["question", "topic"]]
    vector = TfidfVectorizer(norm=False) # Do not normalize.
    vector = TfidfVectorizer(norm=None, min_df = 0.01, stop_words={"english"}) 
    vector.fit(df2['question']) # This determines the vocabulary.

    vectorOut = open("tfidf_topic.pkl", "wb")
    pickle.dump(vector, vectorOut)
    vectorOut.close()

    tf_idf_sparse = vector.transform(df2['question'])
    questions = pd.DataFrame(tf_idf_sparse.todense())
    questions.columns = vector.vocabulary_
    scaler = StandardScaler()
    scaler.fit(questions)

    scaler_out = open("scaling_topic.pkl", "wb")
    pickle.dump(scaler, scaler_out)
    scaler_out.close()

    questions_sc = scaler.transform(questions)
    max = 0
    all = []
    for n in range(50, questions.shape[1] + 1):
        pca = PCA(n_components=n)
        pca.fit(questions_sc) 
        pcaq = pca.transform(questions_sc)
        cv = []
        for k in range(5):
            clf = svm.SVC()

            X_train, X_test, y_train, y_test = train_test_split(pcaq,
                                                                df2['topic'].values,
                                                                test_size = .25)
            clf = clf.fit(X_train, y_train)
            ypreds = clf.predict(X_test)
            scores = precision_recall_fscore_support(y_test,ypreds)[2]
            cv.append(scores)
        cv = np.array(cv)
        cvdf = pd.DataFrame(cv)
        scores = (cvdf.sum()/cvdf.shape[0])

        # bg = BaggingClassifier(clf, max_samples=0.25, max_features=1, n_estimators=30)
        # bg = AdaBoostClassifier(clf, n_estimators=10, learning_rate=1)
        # bg.fit(X_train, y_train)
        # ypreds = bg.predict(X_test)
        # scores = bg.score(X_test, y_test)
        # clf = clf.fit(X_train, y_train)
        # ypreds = clf.predict(X_test)
        # scores = precision_recall_fscore_support(y_test,ypreds)[2]

        if scores[1] > max:
            max = scores[1]
        print(n, scores[1], df2.topic.unique()[1])
        all.append((n, scores))
    print("MAX: ", max, "\n")
    maximums = []
    for j in all:
        if j[1][1] == max:
            maximums.append(j)
    bests = []
    for j in maximums:
        score = (j[0],scorer(j[1]))
        bests.append(score)
    print(bests)

    n_best = None
    best_score = 0
    for j in bests:
        if j[1] > best_score:
            best_score = j[1]
            n_best = j[0]
    print()
    print("BESTS: ",n_best, best_score)

    # Doing optimal pca
    pca = PCA(n_components=n_best)
    pca.fit(questions_sc)
    pca_out = open("pca_topic.pkl", "wb")
    pickle.dump(pca, pca_out)
    pca_out.close()
    pcaq = pca.transform(questions_sc)

    #clf = tree.DecisionTreeClassifier()
    cv = []
    for i in range(15):
        clf = svm.SVC()

        X_train, X_test, y_train, y_test = train_test_split(pcaq,
                                                            df2['topic'].values,
                                                            test_size = .25)
        clf = clf.fit(X_train, y_train)
        ypreds = clf.predict(X_test)
        scores = precision_recall_fscore_support(y_test,ypreds)[2]
        cv.append(scores)
    cv = np.array(cv)
    cvdf = pd.DataFrame(cv)
    avgf1_perclass = (cvdf.sum()/cvdf.shape[0])
    print("average F1 per class: \n",avgf1_perclass)
    overall_F1 = (avgf1_perclass.sum()/cvdf.shape[1])
    print("overall F1: ", overall_F1)


    clf = svm.SVC()

    X_train, X_test, y_train, y_test = train_test_split(pcaq,
                                                        df2['topic'].values,
                                                        test_size = .25)
    clf = clf.fit(X_train, y_train)
    outputfile = open("topic_pred.pkl", "wb")
    pickle.dump(clf, outputfile)
    outputfile.close()

if __name__ == '__main__':
    main()