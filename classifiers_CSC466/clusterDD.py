import sys
import os
import nltk
from nltk.corpus import stopwords
from nltk.corpus import wordnet as wn
import numpy as np
from sklearn.cluster import KMeans
import sklearn.metrics as sk
import pandas as pd


def getFeatures(record):
    stop_words = ['', 'a', 'able', 'about', 'above', 'abst', 'accordance', 'according', 'accordingly', 'across', 'act', 'actually', 'added', 'adj', 'affected', 'affecting', 'affects', 'after', 'afterwards', 'again', 'against', 'ah', 'all', 'almost', 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'an', 'and', 'announce', 'another', 'any', 'anybody', 'anyhow', 'anymore', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere', 'apparently', 'approximately', 'are', 'aren', 'arent', 'arise', 'around', 'as', 'aside', 'ask', 'asking', 'at', 'auth', 'available', 'away', 'awfully', 'b', 'back', 'be', 'became', 'because', 'become', 'becomes', 'becoming', 'been', 'before', 'beforehand', 'begin', 'beginning', 'beginnings', 'begins', 'behind', 'being', 'believe', 'below', 'beside', 'besides', 'between', 'beyond', 'biol', 'both', 'brief', 'briefly', 'but', 'by', 'c', 'ca', 'came', 'can', 'cannot', "can't", 'cause', 'causes', 'certain', 'certainly', 'co', 'com', 'come', 'comes', 'contain', 'containing', 'contains', 'could', 'couldnt', 'd', 'date', 'did', "didn't", 'different', 'do', 'does', "doesn't", 'doing', 'done', "don't", 'down', 'downwards', 'due', 'during', 'e', 'each', 'ed', 'edu', 'effect', 'eg', 'eight', 'eighty', 'either', 'else', 'elsewhere', 'end', 'ending', 'enough', 'especially', 'et', 'et-al', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'ex', 'except', 'f', 'far', 'few', 'ff', 'fifth', 'first', 'five', 'fix', 'followed', 'following', 'follows', 'for', 'former', 'formerly', 'forth', 'found', 'four', 'from', 'further', 'furthermore', 'g', 'gave', 'get', 'gets', 'getting', 'give', 'given', 'gives', 'giving', 'go', 'goes', 'gone', 'got', 'gotten', 'h', 'had', 'happens', 'hardly', 'has', "hasn't", 'have', "haven't", 'having', 'he', 'hed', 'hence', 'her', 'here', 'hereafter', 'hereby', 'herein', 'heres', 'hereupon', 'hers', 'herself', 'hes', 'hi', 'hid', 'him', 'himself', 'his', 'hither', 'home', 'how', 'howbeit', 'however', 'hundred', 'i', 'id', 'ie', 'if', "i'll", 'im', 'immediate', 'immediately', 'importance', 'important', 'in', 'inc', 'indeed', 'index', 'information', 'instead', 'into', 'invention', 'inward', 'is', "isn't", 'it', 'itd', "it'll", 'its', 'itself', "i've", 'j', 'just', 'k', 'keep\tkeeps', 'kept', 'kg', 'km', 'know', 'known', 'knows', 'l', 'largely', 'last', 'lately', 'later', 'latter', 'latterly', 'least', 'less', 'lest', 'let', 'lets', 'like', 'liked', 'likely', 'line', 'little', "'ll", 'look', 'looking', 'looks', 'ltd', 'm', 'made', 'mainly', 'make', 'makes', 'many', 'may', 'maybe', 'me', 'mean', 'means', 'meantime', 'meanwhile', 'merely', 'mg', 'might', 'million', 'miss', 'ml', 'more', 'moreover', 'most', 'mostly', 'mr', 'mrs', 'much', 'mug', 'must', 'my', 'myself', 'n', 'na', 'name', 'namely', 'nay', 'nd', 'near', 'nearly', 'necessarily', 'necessary', 'need', 'needs', 'neither', 'never', 'nevertheless', 'new', 'next', 'nine', 'ninety', 'no', 'nobody', 'non', 'none', 'nonetheless', 'noone', 'nor', 'normally', 'nos', 'not', 'noted', 'nothing', 'now', 'nowhere', 'o', 'obtain', 'obtained', 'obviously', 'of', 'off', 'often', 'oh', 'ok', 'okay', 'old', 'omitted', 'on', 'once', 'one', 'ones', 'only', 'onto', 'or', 'ord', 'other', 'others', 'otherwise', 'ought', 'our', 'ours', 'ourselves', 'out', 'outside', 'over', 'overall', 'owing', 'own', 'p', 'page', 'pages', 'part', 'particular', 'particularly', 'past', 'per', 'perhaps', 'placed', 'please', 'plus', 'poorly', 'possible', 'possibly', 'potentially', 'pp', 'predominantly', 'present', 'previously', 'primarily', 'probably', 'promptly', 'proud', 'provides', 'put', 'q', 'que', 'quickly', 'quite', 'qv', 'r', 'ran', 'rather', 'rd', 're', 'readily', 'really', 'recent', 'recently', 'ref', 'refs', 'regarding', 'regardless', 'regards', 'related', 'relatively', 'research', 'respectively', 'resulted', 'resulting', 'results', 'right', 'run', 's', 'said', 'same', 'saw', 'say', 'saying', 'says', 'sec', 'section', 'see', 'seeing', 'seem', 'seemed', 'seeming', 'seems', 'seen', 'self', 'selves', 'sent', 'seven', 'several', 'shall', 'she', 'shed', "she'll", 'shes', 'should', "shouldn't", 'show', 'showed', 'shown', 'showns', 'shows', 'significant', 'significantly', 'similar', 'similarly', 'since', 'six', 'slightly', 'so', 'some', 'somebody', 'somehow', 'someone', 'somethan', 'something', 'sometime', 'sometimes', 'somewhat', 'somewhere', 'soon', 'sorry', 'specifically', 'specified', 'specify', 'specifying', 'still', 'stop', 'strongly', 'sub', 'substantially', 'successfully', 'such', 'sufficiently', 'suggest', 'sup', 'sure\tt', 'take', 'taken', 'taking', 'tell', 'tends', 'th', 'than', 'thank', 'thanks', 'thanx', 'that', "that'll", 'thats', "that've", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'thence', 'there', 'thereafter', 'thereby', 'thered', 'therefore', 'therein', "there'll", 'thereof', 'therere', 'theres', 'thereto', 'thereupon', "there've", 'these', 'they', 'theyd', "they'll", 'theyre', "they've", 'think', 'this', 'those', 'thou', 'though', 'thoughh', 'thousand', 'throug', 'through', 'throughout', 'thru', 'thus', 'til', 'tip', 'to', 'together', 'too', 'took', 'toward', 'towards', 'tried', 'tries', 'truly', 'try', 'trying', 'ts', 'twice', 'two', 'u', 'un', 'under', 'unfortunately', 'unless', 'unlike', 'unlikely', 'until', 'unto', 'up', 'upon', 'ups', 'us', 'use', 'used', 'useful', 'usefully', 'usefulness', 'uses', 'using', 'usually', 'v', 'value', 'various', "'ve", 'very', 'via', 'viz', 'vol', 'vols', 'vs', 'w', 'want', 'wants', 'was', 'wasnt', 'way', 'we', 'wed', 'welcome', "we'll", 'went', 'were', 'werent', "we've", 'what', 'whatever', "what'll", 'whats', 'when', 'whence', 'whenever', 'where', 'whereafter', 'whereas', 'whereby', 'wherein', 'wheres', 'whereupon', 'wherever', 'whether', 'which', 'while', 'whim', 'whither', 'who', 'whod', 'whoever', 'whole', "who'll", 'whom', 'whomever', 'whos', 'whose', 'why', 'widely', 'willing', 'wish', 'with', 'within', 'without', 'wont', 'words', 'world', 'would', 'wouldnt', 'www', 'x', 'y', 'yes', 'yet', 'you', 'youd', "you'll", 'your', 'youre', 'yours', 'yourself', 'yourselves', "you've", 'z', 'zero']
    important_words = {"Agriculture": ["water","drought","crop","agricultur","irrig","farmer"], "Government": ["depart","senate","govern","civic","voter","elect","assembl","roll","senat","presid","colleagu","resolut"],"Culture":["art","baseball","creativ","cultur","artist"],"Environment":["oil","spill","protect","emiss","cell","carbon"],"Health":["health","patient","emerg","disast","surg","healthcar","hospit","nurs","midwiv","physician","clinic","medic"],"Economy":["house","afford","homeless","bond","bail","insurance","bankruptci","exempt","delta","invest","fund","local","afford"],"Family":["care","youth","licens","children","child","famili","parent","foster","health","community","opportun"], "Transportation":["car","recall","consum","dealer","vehicl","driver","transport","tire","rubber","turf","transit","wast","road","mainten","vehicl","fuel","electr","technolog","reduct","hydrogen","goal"],"Jobs":["civil", "workforce","opportun","employ","job", "divers","hire","recruit","employer"],"Education":["school","education","teacher","student","educ","district","special","kid","youth"],"Veterans":["veteran","benefit","mental","hous"],"Smoking":["tobacco","smoke","vape","vapor","nicotin","e-cigarett"]}
    row = {}
    words = nltk.word_tokenize(record)
    POS = nltk.pos_tag(words)
    prop_nouns=0
    verbs = 0
    adjs = 0
    nouns = 0
    lene = 0
    ayes = 0
    for word in words:
        lene += len(word)
    for tag in POS:
        if tag[1] in ['NNP', 'NNPS'] and tag[0].lower() not in stop_words:
            prop_nouns +=1
        elif tag[1] in ['NN','NNS']:
            nouns += 1
        elif tag[1] in ['VB','VBD','VBG','VBN','VBP','VBZ']:
            verbs += 1
        elif tag[1] in ['JJ','JJR','JJS']:
            adjs+= 1
    #count proportion of nouns, verbs, propernouns, adjectives
    row["prop_prop_nouns"] = prop_nouns/len(words)
    row['prop_improp_nouns'] = nouns/len(words)
    row['prop_adjs'] =adjs/len(words)
    row['prop_verbs']= verbs/len(words)

    words = [word.lower() for word in words if word not in ".,!$%^&*()_+-=\{\}|[]\\<>?,/:;\"`~"]
    words = [w for w in words if w not in stop_words]
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
   
def myKM(data, k, e):
  t = 0
  n = len(data)
  rowidxs = [i for i in range(len(data))]
  init_centroids = []
  while len(init_centroids) < k:
    newelem = data[np.random.choice(rowidxs)][0]
    if newelem not in init_centroids:
      init_centroids.append(newelem)
  
  error = float("inf")
  clusters = {0:init_centroids}
  current_means = clusters[0]
  attributes = set()
  for y in data:
    for key in y[0].keys():
      attributes.update([key])
  while(error > e):
    t = t + 1
    Cj = []
    for c in range(k):
      Cj.append([])
    for y in data:
      x = y[0]
      distances = []
      for mu in current_means: 
        dist = 0
        myflag = True
        for attr in attributes:
          if attr in x.keys() and attr in mu.keys():
            dist += (x[attr] - mu[attr])**2
          elif attr in x.keys():
            myflag = False
            dist += (x[attr])**2
          elif attr in mu.keys():
            dist += (mu[attr])**2
            myflag = False
          else:
            myflag=False
        distances.append(np.sqrt(dist))
      minind = distances.index(min(distances))
      Cj[minind].append((x,y[1]))
    new_clusters = []
    for cluster in Cj:
        card_inv = 1/len(cluster)
        point_sum = {}
        #point sum initialization
        for po in cluster:
          p = po[0]
          for key in p.keys():
            if key in point_sum:
              point_sum[key]+= p[key]
            else: 
              point_sum[key] = p[key]
        for i in point_sum:
          point_sum[i] = point_sum[i]*card_inv
        new_clusters.append(point_sum)
    clusters[t] = new_clusters
    current_means = new_clusters
    error = 0
    for i in range(k):
      dist =0
      clust1attr = set()
      for attr in clusters[t][i].keys():
        clust1attr.update([attr])
      clust2attr = clust1attr.copy()
      for attr2 in clusters[t-1][i].keys():
        clust2attr.update([attr2])
      for key in clust2attr:
        if key in clusters[t][i].keys() and key in clusters[t-1][i].keys():
          dist += (clusters[t][i][key] - clusters[t-1][i][key])**2
        elif key in clusters[t][i].keys():
          dist += (clusters[t][i][key])**2
        else:
          dist += (clusters[t-1][i][key])**2
      error = error + dist
  #Investigating the closeness between means based on the top values
  for meanPt in current_means:
    values = sorted(meanPt.items(), key = lambda kv:(kv[1], kv[0]), reverse = True)
    output = []
    for i in range(3):
      output.append(values[i])
    #uncomment below to see the top three feature values in each cluster mean
    #print("OUTPUT: " + str(output))
  myKMMod = {}
  for clust in Cj:
    myKMMod[Cj.index(clust)] = len(clust)
  return current_means, Cj, myKMMod
    
def main():
    f = sys.argv[1]
    data = []
    data2 = []
    # 30863 LINES IN DATA
    sub = 7715
    fin = open(f, 'r', encoding = "ISO-8859-1")
    fin.readline()
    i = 0
    trues = []
    for line in fin:
       l = line.split("\t")
       text = l[14]
       true = l[2]
       trues.append(true)
       features = getFeatures(text)
       data.append((features,true))
       data2.append(features)
       i += 1
       if i == sub:
           break
    fin.close()
    
    
    #Sets k to the number of target variable classes
    k = len(set(trues))
    mydf = pd.DataFrame(data2).fillna(0)
    
    scores = []
    Cs = []
    classCounts = []

    for run in range(7):
      some = myKM(data, k=k, e = 0.000000001)
      kmeans = KMeans(n_clusters=k, n_init=1,init=np.array(mydf[:k]),random_state=0,tol=0.01).fit(np.array(mydf))
      
      #Prints the average distance betweeen the final centroids of the manual Kmeans, and the scikit learn Kmeans
      #print("Average distance between final centroids of manual and scikitLearn Kmeans: " + str(np.mean(np.sqrt(np.sum(np.array(np.array(kmeans.cluster_centers_) - pd.DataFrame(some[0]).fillna(0))**2, axis = 1)))))
      
      #Number of points classified for each cluster in SciKit Learn Model
      sciKitMod ={i: len(np.where(kmeans.labels_ == i)[0]) for i in range(kmeans.n_clusters)}

  
      partitioncounts = {}
      for c in some[1]:
          for p in c: 
              if p[1] in partitioncounts.keys():
                  partitioncounts[p[1]] += 1
              else: 
                  partitioncounts[p[1]] = 1
      F = 0
      for c in some[1]:
          counts = {}
          for p in c:
              if p[1] in counts.keys():
                  counts[p[1]] = counts[p[1]] + 1
              else: 
                  counts[p[1]] = 1
          maxkey = ""
          maxcount = 0
          totalcount = 0
          for x,y in counts.items():
              totalcount += y
              if y > maxcount:
                  maxkey = x
                  maxcount = y
          partitioncount = partitioncounts[maxkey]
          F += (2 * maxcount)/(totalcount + partitioncount)
          F1 = F/k
          scores.append(F1)
          Cs.append(some[1])
          classCounts.append(some[2])
    bestClusts = Cs[scores.index(max(scores))]
    bests = []
    max_classes = []
    trues_preds = []
    for clust in bestClusts:
      pred_counts = {}
      for p in clust:
        if p[1] in pred_counts.keys():
          pred_counts[p[1]] += 1
        else:
          pred_counts[p[1]] = 1
      best = 0
      max_class = ''
      for _class in pred_counts.keys():
        if pred_counts[_class] > best:
          best = pred_counts[_class]
          max_class = _class
      bests.append(best)
      max_classes.append(max_class)
      for p in clust:
        true1 = p[1]
        pred = max_class
        trues_preds.append((true1, pred))

    

    Ts = []
    Prs = []
    for tup in trues_preds:
      Ts.append(tup[0])
      Prs.append(tup[1])

    print("\n\nCLUSTER CARDINALITY FOR BEST CLUSTERS: ")
    print(classCounts[scores.index(max(scores))])
    print("\n\n\nCONFUSION MATRIX: ")
    print("\n",max_classes)
    print(sk.confusion_matrix(Ts, Prs, labels=max_classes))

    




    print("\n\nBest myKM accuracy after 7 runs: " + str(max(scores)) + "\n")
       
if __name__ == "__main__":
    main()
