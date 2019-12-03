import sys
import os
import nltk
from nltk.corpus import stopwords
import numpy as np
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
import sklearn.metrics as sk
import pandas as pd
import math
import random

class Leaf:
    def __init__ (self, df, data, from_, to, class_, class_counts):
        self.data = data
        self.df = df
        self.from_ = from_
        self.to = to
        self.class_ = class_
        self.class_counts = class_counts

def print_tree(node, limit=float("inf")):
    count = 0
    for y in node.to:
        count+= 1
        if y.to and count <=limit:
            print("rule" + str(y.data))
            print_tree(y)
        else:
            print("predicted class:" + str(y.class_))
            terminalData = y.df['target'].value_counts().to_dict()

def getFeatures(record):
    important_words = {"Agriculture": ["water","drought","crop","agricultur","irrig","farmer"], "Government": ["depart","senate","govern","civic","voter","elect","assembl","roll","senat","presid","colleagu","resolut"],"Culture":["art","baseball","creativ","cultur","artist"],"Environment":["oil","spill","protect","emiss","cell","carbon"],"Health":["health","patient","emerg","disast","surg","healthcar","hospit","nurs","midwiv","physician","clinic","medic"],"Economy":["house","afford","homeless","bond","bail","insurance","bankruptci","exempt","delta","invest","fund","local","afford"],"Family":["care","youth","licens","children","child","famili","parent","foster","health","community","opportun"], "Transportation":["car","recall","consum","dealer","vehicl","driver","transport","tire","rubber","turf","transit","wast","road","mainten","vehicl","fuel","electr","technolog","reduct","hydrogen","goal"],"Jobs":["civil", "workforce","opportun","employ","job", "divers","hire","recruit","employer"],"Education":["school","education","teacher","student","educ","district","special","kid","youth"],"Veterans":["veteran","benefit","mental","hous"],"Smoking":["tobacco","smoke","vape","vapor","nicotin","e-cigarett"]}
    row = {}
    words = nltk.word_tokenize(record)
    lene = 0
    numwords = 0
    words = [word.lower() for word in words if word not in ".,!$%^&*()_+-=\{\}|[]\\<>?,/:;\"`~"]
    porter_stemmer = nltk.stem.porter.PorterStemmer()
    words = [porter_stemmer.stem(word) for word in words]
    for w in words:
        for key, val in important_words.items():
            if w in val:
                if key in row.keys():
                    row[key] += 1
                else:
                    row[key] = 1
    return row

def DT (data, nu, pi, from_ = Leaf(None, None, None, None, None, None),rec_count = 0, first_node = None):
    if first_node == None:
        first_node = from_
    n = len(data)
    vals = list(data['target'].unique())
    ni = {} 
    for val in vals: 
        temp = data[data['target'] == val]
        ni[val] = len(temp) 
    maxPur = -1
    maxPurID = 0
    for i,j in ni.items():
        if j > maxPur:
            maxPur = j
            maxPurID = i
    purityD = (maxPur/n, maxPurID) 
    if n <= nu or purityD[0] >= pi:
        from_.class_ = maxPurID
        return first_node 
    splitter = ([], 0)
    flag = False
    for Xj in list(data.drop("target",axis=1).columns):
        if (len(data[Xj].unique()) >= 2): 
            v_score = evaluation(data, Xj)
            if v_score[1] > splitter[1]:
                flag = True
                splitter = v_score
    rec_count+=1
    if flag:
        Dy = data[data[splitter[0][0]] <= splitter[0][2]]
        Dn = data[data[splitter[0][0]] > splitter[0][2]]
        NodeDy = Leaf(Dy, [splitter[0][0], '<=', splitter[0][2]], from_, None, 0, None)
        NodeDn = Leaf(Dn, [splitter[0][0], '>', splitter[0][2]], from_, None, 0, None)
        from_.to = [NodeDy, NodeDn]
        x = DT(Dy, nu, pi, from_=NodeDy, rec_count = rec_count,first_node = from_)
        y= DT(Dn, nu, pi, from_=NodeDn, rec_count=rec_count, first_node = from_) 
    else: 
        from_.class_ = maxPurID
    return first_node

def evaluation(data, Xj):
    data = data.sort_values(by=Xj).reset_index()
    M = []
    ni = {}
    Nvi = {}
    PDY = []
    PDN = []
    PD = []
    for j in range(len(data)-1):
        if data['target'][j] in ni.keys():
            ni[data['target'][j]] += 1
        else:
            ni[data['target'][j]] = 1
        if data[Xj][j+1] != data[Xj][j]:
            v = (int(data[Xj][j+1]) + int(data[Xj][j]))/2
            M.append(v)
            vi = {}
            PDYsum_1 = 0
            PDY_nums = []
            PDNsum_1 = 0
            PDN_nums = []
            for i in data['target'].unique():
                temp = data[np.logical_and(data['target'] == i,data[Xj] <= v)]
                temp2 = data[np.logical_and(data['target'] == i,data[Xj] > v)]
                vi[i] = len(temp)
                PDYsum_1 += vi[i]
                PDY_nums.append(vi[i])
                PDNsum_1 += len(temp2)
                PDN_nums.append(len(temp2))
            temp = np.array(PDY_nums)/PDYsum_1
            PDY.append(temp)
            temp2 = np.array(PDN_nums)/PDYsum_1
            PDN.append(temp2)
            Nvi[v] = vi
    if data['target'][len(data)-1] in ni.keys():
        ni[data['target'][len(data)-1]] += 1
    else:
        ni[data['target'][len(data)-1]] = 1 
    for i in data['target'].unique():
        PD.append(ni[i]/len(data))
    vStar = ([], 0)
    nj_sum = np.sum(np.array(ni.values()))
    for m in range(len(M)):
        Nvj_sum = np.sum(np.array(Nvi[M[m]].values()))
        HD = np.sum(np.multiply(np.array(PD), np.log2(np.array(PD))))
        HDY = 0 
        HDN = 0
        for j in PDY[m]:
            if j != 0:
                HDY += j*math.log(j,2)
        for k in PDN[m]:
            if k != 0:
                HDN += k*math.log(k,2)
        HD = (-1) * HD
        HDY = (-1) * HDY
        HDN = (-1) * HDN
        HDYDN = (len(data[data[Xj] <= M[m]])/len(data))*HDY + (len(data[data[Xj] > M[m]])/len(data))*HDN
        Gain = HD - HDYDN
        if Gain > vStar[1]:
            vStar = ([Xj, '<=', M[m]], Gain)
    return vStar 

def test_data(test,node,result={}, pred={}):
    if node.to:
        crit = node.to[0].data
        split_1 = test[test[crit[0]] <= crit[2]]
        split_2 = test[test[crit[0]] > crit[2]]
        x={}
        y={}
        if len(split_1) > 0:
            result,pred = test_data(split_1, node.to[0], result, pred)
        if len(split_2) > 0:
            result,pred = test_data(split_2, node.to[1], result, pred)
        return result,pred
    else:
        cluster = str(node.class_)
        true = test['target'].value_counts().to_dict()
        if cluster in pred.keys():
            pred[cluster] += len(test)
        else:
            pred[cluster] = len(test)
        if cluster in true.keys():
            if cluster in result.keys():
                result[cluster] += true[cluster]
            else:
                result[cluster] = true[cluster]
        return result,pred
    
def main():
    f = sys.argv[1]
    hFlag = False
    if len(sys.argv) > 2 and sys.argv[2]=='-h':
        hFlag = True
    data2 = []
    fin = open(f, 'r')
    fin.readline()
    i = 0
    trues = []
    hearingTexts = {}
    for line in fin:
       l = line.split("\t")
       text = l[14]
       true = l[2]
       if hFlag:
           hearing = l[5]
           if (true, hearing) in hearingTexts.keys():
               hearingTexts[(true,hearing)]+= " "+text
           else:
               hearingTexts[(true,hearing)] =text
       else: 
           trues.append(true)
           features = getFeatures(text)
           data2.append(features)
    if hFlag:
        hearing_counts= {}
        keep_committees = []
        for h in hearingTexts.keys():
            if h[0] in hearing_counts.keys():
                hearing_counts[h[0]] += 1
            else:
                hearing_counts[h[0]] = 1
        for committ in hearing_counts.keys():
            if hearing_counts[committ] > 1:
                keep_committees.append(committ)
        for h in hearingTexts.keys():
            if h[0] in keep_committees:
                trues.append(h[0])
                features = getFeatures(hearingTexts[h])
                data2.append(features)
    fin.close()
    mydf = pd.DataFrame(data2).fillna(0)
    mydf['target'] = trues
    if hFlag:
        testidx = []
        trainidx = []
        for comm in mydf['target'].unique():
            idxs = list(mydf[mydf['target']== comm].index.values)
            random.shuffle(idxs)
            test_split = max(int(len(idxs)/4),1)
            testidx.extend(idxs[:test_split])
            trainidx.extend(idxs[test_split:])
        df_train = mydf.iloc[trainidx,:]
        df_test = mydf.iloc[testidx,:]
    else:
        X= mydf.drop('target',axis=1)
        y = mydf['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3)
        df_train = pd.concat([X_train, y_train], axis=1)
        df_test = pd.concat([X_test,y_test],axis=1)
    pur = 6
    if hFlag:
        pur = 1
    x =DT(df_train, pur, 0.9)
    result,pred = test_data(df_test,x)
    F_sum = 0
    print("Number of records = " + str(len(mydf))+ " (" + str(len(df_train)) + " train, " + str(len(df_test)) + " test)")
    print("Number of labels = " + str(len(df_test['target'].unique())))
    print("Labels: " + str(df_test['target'].unique()))
    for j in df_test['target'].unique():
        print("Metrics for Committee " + str(j) +  ": ")
        if j in pred.keys():
            if j not in result.keys():
                result[j] = 0
            Fni = len(df_test[df_test['target']==j])
            recall = result[j] / Fni
            prec = result[j] / pred[j]
            F = 2* result[j] / (Fni + pred[j])
        else:
            recall = prec = F = 0.0
        print("\tPrecision = " + str(prec))
        print("\tRecall = " + str(recall))
        print("\tF1 score: " + str(F))
        F_sum += F
    acc = sum(result.values())/len(df_test)
    F = F_sum * (1/len(df_test['target'].unique()))
    print("Overall Accuracy: " + str(acc))
    print("Overall F: "+str(F))
 
if __name__ == "__main__":
    main()