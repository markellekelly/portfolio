import sys
import pymysql.cursors
import pandas as pd
import numpy as np
import nltk
import spacy
import re
import sklearn as sk
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import cross_val_score
import pickle
from nameparser import HumanName
from nltk.corpus import wordnet as wn
from spacy.tokens import Token
import pymysql.cursors
import datetime
from decimal import *
def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn

def chooser(dict,names,topic_matter):
    if topic_matter == 'Schedule':
        scheduleText(dict,names)
    if topic_matter == 'clubs':
        clubText(dict,names)
    if topic_matter == 'Courses':
        courseText(dict,names)
    if topic_matter == 'instructors':
        instructorText(dict,names)
    if topic_matter == 'publications':
        publicationText(dict,names)
    if topic_matter == 'ratings':
        ratingsText(dict,names)
    if topic_matter == 'researchinterests':
        researchText(dict,names)
    if topic_matter == 'seniorprojects':
        seniorprojectText(dict,names)
    if topic_matter == 'tenureinformation':
        tenureinformationText(dict,names)
    if topic_matter == 'degrees':
        degreeText(dict,names)

def matchNames(entries):
    name_set = set()
    if 'FirstName' in entries[0] or 'LastName' in entries[0]:
        for an_entry in entries:
            builder_string = []
            if 'FirstName' in an_entry:
                builder_string.append(an_entry['FirstName'])
            else:
                builder_string.append('')
            if 'LastName' in an_entry:
                builder_string.append(an_entry['LastName'])
            else:
                builder_string.append('')

            name_set.add(tuple(builder_string))

    FirstName = 0
    LastName = 0

    for e in name_set:
        break
    if e[0] != '':
        FirstName = 1
    if e[1] != '':
        LastName = 1

    value_dict = dict()
    for name in name_set:
        if FirstName == 1 and LastName == 1:
            value_dict[name[0] + ' ' + name[1]] = []
            for a_dict in entries:
                if a_dict['FirstName'] == name[0] and a_dict['LastName'] == name[1]:
                    value_dict[name[0] + ' ' + name[1]].append(a_dict)
    if FirstName == 1 and LastName == 0:
        value_dict[name[0]] = []
        for a_dict in entries:
            if a_dict['FirstName'] == name[0]:
                value_dict[name[0]].append(a_dict)
    if FirstName == 0 and LastName == 1:
        value_dict[name[1]] = []
        for a_dict in entries:
            if a_dict['LastName'] == name[1]:
                value_dict[name[1]].append(a_dict)
    return value_dict

def clubText(a_dict,names):
    if names:
        for getter in a_dict:
            key_set = set(a_dict[getter][0].keys())
            break
        if 'FirstName' in key_set:
            key_set.remove('FirstName')
        if 'LastName' in key_set:
            key_set.remove('LastName')
        for item in a_dict:
            buildstring = ''
            buildstring += item + ' is an advisor '
            for entry in a_dict[item]:
                if 'clubname' in entry:
                    buildstring += ' for ' + entry['clubname'] + ' '
                if len(key_set) > 0:
                    buildstring += ','
            buildstring = buildstring.replace(' ,',', ')
            if len(key_set) > 0:
                print(' '.join(buildstring.split())[:-1])
            else:
                print(' '.join(buildstring.split()))
    else:
        print('The club(s) that match your query are:')
        for entry in a_dict:
            buildstring = ''
            if 'clubname' in entry:
                buildstring += ' ' + entry['clubname'] + ' '
            buildstring += ','
            buildstring = buildstring.replace(' ,',', ')
            print(' '.join(buildstring.split())[:-1])

def courseText(a_dict,names):
    if names:
        for getter in a_dict:
            key_set = set(a_dict[getter][0].keys())
            break
        if 'FirstName' in key_set:
            key_set.remove('FirstName')
        if 'LastName' in key_set:
            key_set.remove('LastName')
        for item in a_dict:
            buildstring = ''
            buildstring += item + ' has average grades '
            for entry in a_dict[item]:
                if 'averagegrade' in entry:
                    if entry['averagegrade'] == 0:
                        buildstring += ' unknown '
                    else:
                        buildstring += ' ' + str(entry['averagegrade'] * 100) + ' '
                if 'Courses' in entry:
                    buildstring += ' for ' + entry['Courses']
                    if 'courseName' in entry:
                        if entry['courseName'] is not None:
                            buildstring += '-' + entry['courseName']
                if len(key_set) > 0:
                    buildstring += ','
            buildstring = buildstring.replace(' ,',', ')
            if len(key_set) > 0:
                print(' '.join(buildstring.split())[:-1])
            else:
                print(' '.join(buildstring.split()))
    else:
        print('The rating(s) that match your query are:')
        for entry in a_dict:
            buildstring = ''
            if 'averagegrade' in entry:
                if entry['averagegrade'] == 0:
                    buildstring += ' unknown '
                else:
                    buildstring += ' ' + str(entry['averagegrade'] * 100) + ' '
            if 'Courses' in entry:
                buildstring += ' for ' + entry['Courses']
                if 'courseName' in entry:
                    if entry['courseName'] is not None:
                        buildstring += '-' + entry['courseName']
            buildstring += ','
            buildstring = buildstring.replace(' ,',', ')
            print(' '.join(buildstring.split())[:-1])

def degreeText(a_dict,names):
    if names:
        for getter in a_dict:
            key_set = set(a_dict[getter][0].keys())
            break
        if 'FirstName' in key_set:
            key_set.remove('FirstName')
        if 'LastName' in key_set:
            key_set.remove('LastName')
        for item in a_dict:
            buildstring = ''
            buildstring += item
            for entry in a_dict[item]:
                if 'degreetype' in entry:
                    buildstring += ' has a ' + entry['degreetype'] + ' '
                if 'university' in entry:
                    buildstring += ' from ' + entry['university'] + ' '
                if 'startdate' in entry:
                    buildstring += ' in ' + entry['startdate'] + ' '
                if len(key_set) > 0:
                    buildstring += ','
            buildstring = buildstring.replace(' ,',', ')
            if len(key_set) > 0:
                print(' '.join(buildstring.split())[:-1])
            else:
                print(' '.join(buildstring.split()))
    else:
        print('The degree(s) that match your query are:')
        for entry in a_dict:
            buildstring = ''
            if 'degreetype' in entry:
                buildstring += ' a ' + entry['degreetype'] + ' '
            if 'university' in entry:
                buildstring += ' from ' + entry['university'] + ' '
            if 'startdate' in entry:
                buildstring += ' in ' + entry['startdate'] + ' '
            buildstring += ','
            buildstring = buildstring.replace(' ,',', ')
            print(' '.join(buildstring.split())[:-1])

def instructorText(a_dict,names):
    if names:
        for getter in a_dict:
            key_set = set(a_dict[getter][0].keys())
            break
        if 'FirstName' in key_set:
            key_set.remove('FirstName')
        if 'LastName' in key_set:
            key_set.remove('LastName')
        for item in a_dict:
            buildstring = ''
            buildstring += item + ' '
            for entry in a_dict[item]:
                if 'position' in entry:
                    buildstring += ' a ' + entry['position']
                if 'chair' in entry:
                    if entry['chair']:
                        buildstring += ' is the chair '
                if 'room' in entry:
                    buildstring += ' has room ' + entry['room']
                if 'phone' in entry:
                    buildstring += ' can be called at ' + entry['phone']
                if 'email' in entry:
                    buildstring +=  ' can be emailed at ' + entry['email']
                if 'url' in entry:
                    if entry['url'] != None:
                        buildstring += ' can be found online at ' + entry['url']
            buildstring = buildstring.replace(' ,',', ')
            print(' '.join(buildstring.split()))
    else:
        print('The matching instructor(s):')
        for entry in a_dict:
            buildstring = ''
            if 'position' in entry:
                buildstring += ' a ' + entry['position']
            if 'chair' in entry:
                if entry['chair']:
                    buildstring += ' is the chair '
            if 'room' in entry:
                buildstring += ' has room ' + entry['room']
            if 'phone' in entry:
                buildstring += ' can be called at ' + entry['phone']
            if 'email' in entry:
                buildstring +=  ' can be emailed at ' + entry['email']
            if 'url' in entry:
                if entry['url'] != None:
                    buildstring += ' can be found online at ' + entry['url']
            buildstring = buildstring.replace(' ,',', ')
            print(' '.join(buildstring.split()))

def publicationText(a_dict,names):
    if names:
        for getter in a_dict:
            key_set = set(a_dict[getter][0].keys())
            break
        if 'FirstName' in key_set:
            key_set.remove('FirstName')
        if 'LastName' in key_set:
            key_set.remove('LastName')
        for item in a_dict:
            buildstring = ''
            buildstring += item + ' wrote '
            for entry in a_dict[item]:
                if 'papername' in entry:
                    buildstring += ' ' + entry['papername'] + ' '
                if 'journalname' in entry:
                    buildstring += ' in ' + entry['journalname'] + ' '
                if len(key_set) > 0:
                    buildstring += ','
            buildstring = buildstring.replace(' ,',', ')
            if len(key_set) > 0:
                print(' '.join(buildstring.split())[:-1])
            else:
                print(' '.join(buildstring.split()) + ' that')
    else:
        print('The publication(s) that match your query are:')
        for entry in a_dict:
            buildstring = ''
            if 'papername' in entry:
                buildstring += ' ' + entry['papername'] + ' '
            if 'journalname' in entry:
                buildstring += ' in ' + entry['journalname'] + ' '
            buildstring += ','
            buildstring = buildstring.replace(' ,',', ')
            print(' '.join(buildstring.split())[:-1])

def ratingsText(a_dict,names):
    if names:
        for getter in a_dict:
            key_set = set(a_dict[getter][0].keys())
            break
        if 'FirstName' in key_set:
            key_set.remove('FirstName')
        if 'LastName' in key_set:
            key_set.remove('LastName')
        for item in a_dict:
            buildstring = ''
            buildstring += item
            for entry in a_dict[item]:
                if 'polyrating' in entry:
                    buildstring += ' has a rating of ' + str(entry['polyrating']) + ' out of 4 '
                if 'numratings' in entry:
                    buildstring += ' based on ' + str(entry['numratings']) + ' ratings '
                if len(key_set) > 0:
                    buildstring += ','
            buildstring = buildstring.replace(' ,',', ')
            if len(key_set) > 0:
                print(' '.join(buildstring.split())[:-1])
            else:
                print(' '.join(buildstring.split()))
    else:
        print('The rating(s) that match your query are:')
        for entry in a_dict:
            buildstring = ''
            if 'polyrating' in entry:
                buildstring += ' a rating of ' + str(entry['polyrating']) + ' out of 4 '
            if 'numratings' in entry:
                buildstring += ' based on ' + str(entry['numratings']) + ' ratings '
            buildstring += ','
            buildstring = buildstring.replace(' ,',', ')
            print(' '.join(buildstring.split())[:-1])

def researchText(a_dict,names):
    if names:
        for getter in a_dict:
            key_set = set(a_dict[getter][0].keys())
            break
        if 'FirstName' in key_set:
            key_set.remove('FirstName')
        if 'LastName' in key_set:
            key_set.remove('LastName')
        for item in a_dict:
            buildstring = ''
            buildstring += item + ' is researching '
            for entry in a_dict[item]:
                for a_key in key_set:
                    buildstring += entry[a_key] + ' , '
            buildstring = buildstring.replace(' ,',', ')
            if len(key_set) > 0:
                print(' '.join(buildstring.split())[:-1])
            else:
                print(' '.join(buildstring.split()) + ' that')

    else:
        print('The matching research interests are',end=' ')
        for item in a_dict:
            print(item['researchinterests'], end=' ')

def scheduleText(a_dict,names):
    if names:
        for getter in a_dict:
            key_set = set(a_dict[getter][0].keys())
            break
        if 'FirstName' in key_set:
            key_set.remove('FirstName')
        if 'LastName' in key_set:
            key_set.remove('LastName')
        for item in a_dict:
            buildstring = ''
            buildstring += item + ' does '
            for entry in a_dict[item]:
                if 'Courses' in entry:
                    if entry['Courses'] is not None:
                        if entry['Courses'] != 'NULL':
                            buildstring += entry['Courses'] + ' '
                            if 'Sections' in entry:
                                buildstring += ' section ' + entry['Sections'] + ' '
                            if 'courseName' in entry:
                                buildstring += ' ' + entry['courseName'] + ' '
                if 'Types' in entry:
                    if entry['Types'] is not None:
                        if entry['Types'] == 'Lec':
                            buildstring += ' a lecture '
                        if entry['Types'] == 'Lab':
                            buildstring += ' a lab '
                        if entry['Types'] == 'Ind':
                            buildstring += ' an independent study course '
                        if entry['Types'] == 'Sem':
                            buildstring += ' a seminar '
                        if entry['Types'] == 'Act':
                            buildstring += ' an activity '
                        if entry['Types'] == 'OH':
                            buildstring += ' an office hour '
                if 'Days' in entry:
                    if entry['Days'] is not 'NULL':
                        buildstring += ' on '
                        if 'M' in entry['Days']:
                            buildstring += ' Monday, '
                        if 'T' in entry['Days']:
                            buildstring += ' Tuesday, '
                        if 'W' in entry['Days']:
                            buildstring += ' Wednesday, '
                        if 'R' in entry['Days']:
                            buildstring += ' Thursday, '
                        if 'F' in entry['Days']:
                            buildstring += ' Friday, '
                        buildstring = buildstring[:-2] + ' '
                if 'StartTime' in entry:
                    if entry['StartTime'] is not None:
                        buildstring += ' at ' + entry['StartTime']
                if 'EndTime' in entry:
                     if entry['EndTime'] is not None:
                        buildstring += ' until ' + entry['EndTime']
                if 'Location' in entry:
                     if entry['Location'] is not None:
                        buildstring += ' in ' + entry['Location']
                if 'Quarter' in entry:
                    if entry['Quarter'] is not None:
                        buildstring += ' during ' + entry['Quarter']
                if 'Year' in entry:
                     if entry['Year'] is not None:
                        buildstring += ' ' + entry['Year']
                if len(key_set) > 0:
                    if len(key_set) > 1:
                        buildstring += ','
                    else:
                        if 'Courses' in entry:
                            if entry['Courses'] != 'NULL':
                                buildstring += ','
            buildstring = buildstring.replace(' ,',', ')
            if len(key_set) > 0:
                print(' '.join(buildstring.split())[:-1])
            else:
                print(' '.join(buildstring.split()) + ' that')
    else:
        print('The matching course(s):')
        for entry in a_dict:
            buildstring = ''
            if 'Courses' in entry:
                if entry['Courses'] is not None:
                    if entry['Courses'] != 'NULL':
                        buildstring += entry['Courses'] + ' '
                        if 'Sections' in entry:
                            buildstring += ' section ' + entry['Sections'] + ' '
                        if 'courseName' in entry:
                                buildstring += ' ' + entry['courseName'] + ' '
                    else:
                        if len(entry.keys()) == 1:
                            continue
            if 'Types' in entry:
                if entry['Types'] is not None:
                    if entry['Types'] == 'Lec':
                        buildstring += ' a lecture '
                    if entry['Types'] == 'Lab':
                        buildstring += ' a lab '
                    if entry['Types'] == 'Ind':
                        buildstring += ' an independent study course '
                    if entry['Types'] == 'Sem':
                        buildstring += ' a seminar '
                    if entry['Types'] == 'Act':
                        buildstring += ' an activity '
                    if entry['Types'] == 'OH':
                        buildstring += ' an office hour '
            if 'Days' in entry:
                if entry['Days'] is not 'NULL':
                    buildstring += ' on '
                    if 'M' in entry['Days']:
                        buildstring += ' Monday, '
                    if 'T' in entry['Days']:
                        buildstring += ' Tuesday, '
                    if 'W' in entry['Days']:
                        buildstring += ' Wednesday, '
                    if 'R' in entry['Days']:
                        buildstring += ' Thursday, '
                    if 'F' in entry['Days']:
                        buildstring += ' Friday, '
                    buildstring = buildstring[:-2] + ' '
            if 'StartTime' in entry:
                if entry['StartTime'] is not None:
                    buildstring += ' at ' + entry['StartTime']
            if 'EndTime' in entry:
                if entry['EndTime'] is not None:
                    buildstring += ' until ' + entry['EndTime']
            if 'Location' in entry:
                if entry['Location'] is not None:
                    buildstring += ' in ' + entry['Location']
            if 'Quarter' in entry:
                if entry['Quarter'] is not None:
                    buildstring += ' during ' + entry['Quarter']
            if 'Year' in entry:
                if entry['Year'] is not None:
                    buildstring += ' ' + entry['Year']
            buildstring += ','
            buildstring = buildstring.replace(' ,',', ')
            print(' '.join(buildstring.split())[:-1])

def seniorprojectText(a_dict,names):
    if names:
        for getter in a_dict:
            key_set = set(a_dict[getter][0].keys())
            break
        if 'FirstName' in key_set:
            key_set.remove('FirstName')
        if 'LastName' in key_set:
            key_set.remove('LastName')
        for item in a_dict:
            buildstring = ''
            buildstring += item + ' was an advisor '
            for entry in a_dict[item]:
                if 'projectname' in entry:
                    buildstring += ' for ' + entry['projectname'] + ' '
                if 'studentname' in entry:
                    buildstring += ' by ' + entry['studentname']
                if len(key_set) > 0:
                    buildstring += ','
            buildstring = buildstring.replace(' ,',', ')
            if len(key_set) > 0:
                print(' '.join(buildstring.split())[:-1])
            else:
                print(' '.join(buildstring.split()) + ' for that')
    else:
        print('The senior project(s) that match your query are:')
        for entry in a_dict:
            buildstring = ''
            if 'projectname' in entry:
                    buildstring += entry['projectname'] + ' '
            if 'studentname' in entry:
                buildstring += ' by ' + entry['studentname']
            buildstring = buildstring.replace(' ,',', ')
            buildstring += ','
            print(' '.join(buildstring.split())[:-1])

def tenureinformationText(a_dict,names):
    if names:
        for getter in a_dict:
            key_set = set(a_dict[getter][0].keys())
            break
        if 'FirstName' in key_set:
            key_set.remove('FirstName')
        if 'LastName' in key_set:
            key_set.remove('LastName')
        for item in a_dict:
            buildstring = ''
            buildstring += item
            for entry in a_dict[item]:
                if 'almamater' in entry:
                    buildstring += ' is an alumni of ' + entry['almamater'] + ' '
                if 'startdate' in entry:
                    buildstring += ' started teaching in ' + str(entry['startdate'])
                if 'enddate' in entry:
                    if entry['enddate'] != 2019 and entry['enddate'] != None:
                        buildstring += ' and stopped teaching in ' + str(entry['enddate'])
                    if entry['enddate'] == None:
                        buildstring += ' but we do not know when they stopped teaching '
                if len(key_set) > 0:
                    buildstring += ','
            buildstring = buildstring.replace(' ,',', ')
            if len(key_set) > 0:
                print(' '.join(buildstring.split())[:-1])
            else:
                print(' '.join(buildstring.split()))
    else:
        print('The profesor(s) that match your query are:')
        for entry in a_dict:
            buildstring = ''
            if 'almamater' in entry:
                buildstring += ' an alumni of ' + entry['almamater'] + ' '
            if 'startdate' in entry:
                buildstring += ' started teaching in ' + str(entry['startdate'])
            if 'enddate' in entry:
                if entry['enddate'] != 2019 and entry['enddate'] != None:
                    buildstring += ' and stopped teaching in ' + str(entry['enddate'])
                if entry['enddate'] == None:
                    buildstring += ' but we do not know when they stopped teaching '
            buildstring = buildstring.replace(' ,',', ')
            buildstring += ','
            print(' '.join(buildstring.split())[:-1])

def resultToEnglish(question,sql,result):
  nlp = spacy.load('en')
  doc = nlp(question)

  people = []
  for ent in doc.ents:
    if ent.label_ == 'PERSON':
      people.append(ent.text)

  topic_matter = sql.split('FROM')[1].split(' ')[1]

  if len(result) == 0:
    print("Hmm, I don't seem to know that information about " + topic_matter)
    return

  if 'COUNT(*)' in result[0]:
    if 'how many' in question.lower():
      print('The answer to your question is ' + str(result[0]['COUNT(*)']) + '.')
    elif result[0]['COUNT(*)'] == 0:
      print('No, there is not a matching result for your query about ' + topic_matter)
      print("I thought you were asking a yes/no question, try rephrasing if you were not")
    else:
      print('Yes, there are ' + str(result[0]['COUNT(*)']) + ' matching results for your query about ' + topic_matter)
      print("I thought you were asking a yes/no question, try rephrasing if you were not")
    return

  if 'LastName' in result[0] or 'FirstName' in result[0]:
      converted_dict = matchNames(result)
      chooser(converted_dict,True,topic_matter)
  elif len(people) == 1:
      converted_dict = dict()
      converted_dict[people[0]] = result
      chooser(converted_dict,True,topic_matter)
  else:
      chooser(result,False,topic_matter)

def getFeatures(quest,research_ar,clubs,univ, courseCodes, courseNames, room_list):
  row={}
  porter_stemmer = nltk.stem.porter.PorterStemmer()
  words = [word.lower().replace(".,!$%^&*()_+-=\{\}|[]\\<>?,/:;\"`~","") for word in str(quest).split(" ")] # fix this!
  words = [word.strip("?.!") for word in words if word != ""]
  # from sql: When retrieving from database, split into two, depending on whether it is one word or more
  important_words = {
    'contact':['email',"e-mail",'phone','offic','websit','contact','reach','call', 'now','current','moment', 'am', 'pm'],
    "courses":["class","cours","csc","cpe",'quarter'],
    'history':['degre','college','graduat','univers','emeriti','almuni', 'recent'],
    'research':['journal','research','publish','paper', 'interest', 'expertis', "studi", "field", "concentr", "disciplin"],
    'rating':['rate', 'polyr'],
    "clubs" :["club", "clubs"],
    'jobs':['lectur',"posit"]}
  import_pairs={
    'contact':['office hours','home page', 'where is', "what days" "which days"],
    'rating':['poly ratings', 'poly rating', 'how good', "well liked", " poorly liked" 'how bad', 'good professor', 'bad professor', 'best professor', 'worst professor', "preferred professor", "better professor", "smarter professor", "good teacher", "bad teacher", "take for"],
    'research':['senior project', 'digital commons', 'research interest', "specialize in", "work on", "work about", "working on", "working on", "senior projects","specializes in"],
    'jobs':['assistant professor', 'associate professor','department chair', "teach here", "work here", "job title", "what department", "work for", "last name", "first name"]}
  for i in range(len(words)-1):
    wordpair= words[i] + " " + words[i+1]
    for key, val in import_pairs.items():
      if wordpair in val:
          row[key] =1
          break
  cp = [" California Polytechnic State University, San Luis Obispo "," Cal Poly ", " California Polytechnic State University ", " CP Slo ", " Cal Poly Slo ", " California Polytechnic Slo "]
  
  quest = quest.replace("?", "")
  quest =" "+ quest.lower() + " "
  research_ar.extend([" Software Validation ", " Information Retrieval ", " AI ", " NLP ", " Robots ", " AR ", " Graphics "," Software Maintenance ", " Animation "])
  if any(a.lower() in quest for a in research_ar):
    row["research_area"] = 1
  if any(u.lower() in quest for u in univ):
    if not any(cpu.lower() in quest for cpu in cp):#Should we exclude cal poly?
      row["university"] = 1
  clubs.extend([" ACM ", " Blockchain club ", " Magic club ", " AI club" , " Artificial Intelligence club ", " CS Grad Student Club " , " Game Development Club ", " Hack For Impact ", " Linix Users ", " App Development Club ", " Women in Software ", " Women in Hardware "])
  if any(c.lower() in quest for c in clubs):
    row["clubs"] = 1

  ##Get actual coursenames
  courseNames.extend(["Knowledge and Discovery from Data", "Design and Analysis of Algorithms", "Database Modeling, Design, and Implementation"])
  opinionRatings = ["should i take", "best for", "worst for", "should students take "]
  if any(cc.lower() in quest for cc in courseCodes) or any(cn.lower() in quest for cn in courseNames):
    if any(x.lower() in quest for x in opinionRatings):
      row["rating"] = 1
    else:
      row["courses"] =1
  
  if len(findEmails(quest)[1])!= 0 or len(get_phone_numbers(quest)[1])!= 0 or len(findTime(quest)[1])!= 0 or len(get_room_numbers(quest,room_list)[1]) != 0 or len(findOffices(quest)[1])!=0:
    row["contact"] = 2
  
  if (' did ' in quest and (' study at ' in quest or ' go to ' in quest)):
      row['history']=1
  
  for phrase in cp:
    quest = quest.replace(phrase, " ")
    
  ###HERE BREAKS INTO WORDS
  words = [porter_stemmer.stem(word) for word in words]
  for w in words:
    if (re.match(r"\d+pm",w) or re.match(r"\d+am",w)):
      row['contact'] =1
    for key, val in important_words.items():
        if w in val:
            row[key] =1
            break
  if row == {}:
    if " where is " in quest:
      row["contact"]=1
    else:
      row['notOurs'] =1
  return row

def get_word(token,doc,word):
  for token2 in doc:
    if token2.dep_ == "compound" and token2.head == token:
      word = token2.text + " " + word
      return get_word(token2, doc, word)
  return (token,doc, word)

def get_names(quest,names_list, name_list):
  cond=""
  quest_list = quest.split(" ")
  prof_words = [" professor "," professors "," dr. "," mr."," ms. "," mrs. "," miss "]
  detected_names= []
  detected_name=[]
  names_2 = []
  for i in range(len(quest_list)-1):
    name = quest_list[i] + " " + quest_list[i+1]
    if name in names_list:
      quest = quest.replace(name," ")
      for wr in prof_words:
        quest = quest.replace(wr, " ")
      detected_names.append(name)
  quest_list = quest.split(" ")
  for i in range(len(quest_list)):
    name = quest_list[i]
    if name in name_list:
      quest = quest.replace(name," ")
      for wr in prof_words:
        quest = quest.replace(wr, " ")
      detected_name.append(name)
  if len(detected_names) == 0:
    names_list = [n + "s" for n in names_list]
    name_list = [n+ "s" for n in name_list]
    for i in range(len(quest_list)-1):
      name = quest_list[i] + " " + quest_list[i+1]
      if name in names_list:
        quest = quest.replace(name," ")
        for wr in prof_words:
          quest = quest.replace(wr, " ")
        detected_names.append(name[:-1])
    for i in range(len(quest_list)):
      name = quest_list[i]
      if name in name_list:
        quest = quest.replace(name," ")
        for wr in prof_words:
          quest = quest.replace(wr, " ")
        detected_name.append(name[:-1])
  if len(detected_names) >0:
    for item in detected_names:
      names_2.append(item)
      nrb = HumanName(item)
      fn = nrb.first
      ln = nrb.last
      cond+= "LOWER(FirstName) = " + repr(fn) + " and LOWER(LastName) = " + repr(ln)+ " and "
  if len(detected_name) >0:
    for item in detected_name:
      names_2.append(item)
      cond+= "LOWER(LastName) = " + repr(item)+ " and "
  return (quest, names_2,cond[:-5])

def findQuarter(quest):  
  cond =""
  allRels = []
  cur = datetime.datetime.now()
  curYear = cur.year
  quarters = [" Winter ", " Spring ", " Summer "," Fall "]
  if cur.month >=9 and cur.month<=12:
    curQ = 3
  elif cur.month >=1 and cur.month<=3:
    curQ = 0
  elif cur.month >=4 and cur.month<=6:
    curQ = 1
  else:
    curQ = 2
  
  relation = re.findall(r"in (\d+) quarter", quest)
  relation.extend(re.findall(r"in (\d+) quarters", quest))
  relation.extend(re.findall(r"(\d+) quarters from now", quest))
  if re.match(r" next quarter ",quest):
    quest = quest.replace(" next quarter ", " ")
    relation.append(1)
  for r in relation:
    allRels.append(r)
    final = int(r) + curQ
    q= final % 4
    if final > 3:
      year = curYear + (final//3)
      cond += "Quarter = " + repr(quarters[q].strip()) + " AND Year = " + repr(year) + " AND "
      
  negRel = re.findall(r"(\d+) quarter ago", quest)
  negRel.extend(re.findall(r"(\d+) quarters ago", quest))
  if re.match(r" last quarter ",quest):
    quest = quest.replace(" last quarter ", " ")
    negRel.append(1)
  for r in negRel:
    allRels.append(r)
    final = abs(curQ - int(r)) 
    q= 3 - (final % 4)
    if final > 3:
      year = curYear + (final//3)
      cond += "Quarter = " + repr(quarters[q].strip()) + " AND Year = " + repr(year) + " AND "
  if " fall " in quest:
    cond += "Quarter = 'Fall' AND "
  if " winter " in quest:
    cond += "Quarter = 'Winter' AND "
  if " spring " in quest:
    cond += "Quarter = 'Spring' AND "
  if " summer " in quest:
    cond += "Quarter = 'Summer' AND "
  if len(allRels)!= 0:
    for item in allRels:
      purge = [" "+item + " quarters ago ", " "+item + " quarter ago ", " "+item + " quarters from now ", " in " + item +" quarter from now ", " in " + item + " quarters from now "]
      for phrase in purge:
        quest = quest.replace(phrase, " ")
  return (quest, cond[:-5])
  
def get_possible_names(quest):
  nlp = spacy.load('en')
  doc = nlp(quest)
  names = []
  for ent in doc.ents:
    if ent.label_ == "PERSON":
      names.append(ent.text)
  return names

def get_journals(quest):
  cond = ""
  journal_list = ["journal of field robotics","artificial intelligence in medicine","innovations in systems and software engineering", "journal of systems integration","requirements engineering","ieee software","data and knowledge engineering","cognitive systems research","acm transactions on graphics","computer journal","new library world","artificial intelligence in medicine","literary and linguistic computing","robotica"] #GET FROM SQL? SYNONYMS?
  found=[]
  possible_additions = [" journal "," journal called "," journal named "," journal titled "]
  for x in journal_list:
    if x in quest: 
      quest = quest.replace(x, "")
      found.append(x)
      for end in possible_additions:
        quest = quest.replace(end,"")
  if len(found)>0:
    for item in found:
      cond+= "LOWER(journalname) = " + repr(item) + " or "
  return (quest, cond[:-4])

def get_papers(quest):
  cond = ""
  paper_list = ["a cognitive theory of visual interaction"] 
  found=[]
  possible_beginnings = [" paper "," paper called "," paper named "," paper titled "]
  possible_endings = [" paper "]
  for x in paper_list:
    if x in quest: 
      quest_split = quest.split(x)
      quest_beg = quest_split[0]
      quest_end = quest_split[1]
      found.append(x)
      for end in possible_endings:
        if end in quest_end and (quest_end.index(end)) == 0:
          quest_end = quest_end[quest.index(end)+ len(end):]
      for beg in possible_beginnings:
        if beg in quest_beg and (quest_beg.index(beg) + len(beg) - 1) == len(quest_beg)-1:
          quest_beg = quest_beg[:quest.index(beg)]
      quest = quest_beg + quest_end
  if len(found)>0:
    for item in found :
      cond+= "LOWER(journalname) = " + repr(item) + " or "
  return (quest, cond[:-4])

def get_phone_numbers(quest):
  cond = ""
  phone_list = []
  phone_words = [" office phone number ", " office phone ", " phone number "," phone ","phones "," i call "," call "," telephone number "," telephone "]
  phones1 = re.findall(r"(\D?(\d{3})\D?\D?(\d{3})\D?(\d{4}))",quest)
  for phone in phones1:
    for y in phone_words:
      quest = quest.replace(y," ")
    quest = quest.replace(phone[0]," ")
  for phone in phones1:
    num = phone[1] + phone[2] + phone[3]
    phone_list.append(num)
  phones2 = re.findall(r"(\(\d{3}\) ?|(\d{3})-?(\d{3})-(\d{4}))",quest)
  for phone in phones2:
    for y in phone_words:
      quest = quest.replace(y," ")
    quest = quest.replace(phone[0]," ")
  for phone in phones2:
    num = phone[1] + phone[2] + phone[3]
    phone_list.append(num)
  if len(phone_list)>0:
    for item in phone_list:
      item = item[:3] + "-" + item[3:6] + "-" + item[6:]
      cond+= "phone = " + repr(item) + " or "
  return (quest,cond[:-4])

def get_room_numbers(quest,room_list):
  found=[]
  possible_additions = [" classroom number "," room number "," classroom "," room "," location "]
  for x in room_list:
    if (" " + x + " ") in quest: 
      quest = quest.replace(x," ")
      found.append(x)
      for end in possible_additions:
        quest = quest.replace(end," ")
  cond = []
  for f in found:
    cond.append("Locations = " + repr(f))
  query = " AND ".join(cond)
  return quest, query

def get_senior_proj(quest):
  paper_list = ["gravity evolved"] 
  found=[]
  possible_additions = [" senior project "," project "]
  for x in paper_list:
    if x in quest: 
      quest = quest.replace(x," ")
      found.append(x)
      for end in possible_additions:
        quest = quest.replace(end," ")
  cond = []
  for f in found:
    cond.append("projectname = " + repr(f))
  query = " AND ".join(cond)
  return quest, query
  return quest, var

def get_student_names(quest,student_list):
  found=[]
  names_2=[]
  possible_additions = [" student named "," students "," student "]
  for x in student_list:
    if x in quest: 
      quest=quest.replace(x," ")
      found.append(x.strip())
      for beg in possible_additions:
        quest=quest.replace(beg," ")
  cond = []
  for f in found:
    names_2.append(f)
    cond.append("LOWER(studentname) = " + repr(f))
  query = " AND ".join(cond)
  return quest, names_2, query

def get_university(quest,univ_list):
  found=[]
  synonyms = {"University of California, Davis": [" UCD "," UC Davis ", " Davis "], "University of Maryland College Park":[" UMD College Park ", " University of Maryland ",' UMD '], "Carnegie Mellon University":[" Carnegie Mellon ", " CMU "], "Kettering University":[" Kettering "], "Federal University of Bahia, Brazil":[" University of Bahia "], "Federal University of Rio Grande do Sul, Brazil":[" University of Rio Grande do Sul "], "Ruy Barbosa College, Brazil ":[" Barbosa College "], "Vienna University of Technology, Austria": [" Vienna University ", " Vienna Tech "], "California State University, Fresno":[" University of Fresno "], "Kings College":[" Kings "], "Pennsylvania State University":[" Penn State University ", " Penn State "], "University of California, Irvine":[" Irvine ", " UI "], "University of Maine":[" UMaine "], "Principia College":[" Principia "], "University of California, Santa Barbara":[" UCSB ", " University of Santa Barbra "], "Tabor College":[" Tabor "], "University of Kansas":[" KU ", " Kansas University "], "University of Rome Tor Vergata":[" University of Tor Vergata "], "California Polytechnic State University, San Luis Obispo":[" Cal Poly ", " California Polytechnic State University ", " CP Slo ", " Cal Poly Slo ", " California Polytechnic Slo "], "University of California, Santa Cruz":[" University of Santa Cruz ", " UC Santa Cruz "], "Technical University of Munich":[" TUM "], "Yerevan State University, Republic of Armenia, USSR":[" Yerevan State University "], "Michigan State University":[" MSU ", " Michigan State "], "Xavier University":[" Xavier "], "University of Patras, Greece":[" University of Patras "], "Western Michigan University":[" Western Michigan University ", " WMICH "], "Northeastern University":[" Northeastern ", " Northeastern U "], "Princeton University":[" Princeton "], "Rice University":[" Rice "], "University of California, San Diego":[" University of San Diego ", " UCSD "], "Northwestern University":[" Northwestern ", " Northwestern U "], "University of Sofia":[" Sofia University "], "University of Waterloo":[" UWaterloo "], "California State University, East Bay":[" Cal State East Bay ", " California State East Bay "], "Santa Clara University":[" SCU "], "University of Valencia, Spain":[" University of Valencia "], "Clemson University":[" Clemson U ", " Clemson "], "University of California, Berkeley":[" UC Berkeley "], "Wichita State University":[" Wichita State "], "CS, Oregon State":[" Oregon State ", " Oregon State University ", " OSU "], "University of Notre Dame":[" Notre Dame ", " UND "], "The Johns Hopkins University":[" John Hopkins ", " JHU ", " John Hopkins University "], "California Institute of Technology":[" Cal Tech ", " Cal Tech University ", " CalTech ", " CalTech University "]}
  possible_additions = [" school at "," school ", " university at "," university ", " college at "," college "," attended "]
  for thing in synonyms.keys():
    for univ in synonyms[thing]:
      if univ.lower() in quest:
        quest = quest.replace(univ, " "+ thing+" ")
  for x in univ_list:
    if x.lower() in quest: 
      quest = quest.replace(x," ")
      found.append(x)
      for end in possible_additions:
        quest = quest.replace(end," ")
  cond = []
  for f in found:
    cond.append("LOWER(university) = " + repr(f))
  query = " AND ".join(cond)
  return quest, query

def get_url(quest,url_list):
  found=[]
  url_words = [" url "," personal website "," website "," personal webpage "," webpage "," homepage "]
  for x in url_list:
    if x in quest:
      quest = quest.replace(x, " ")
      found.append(x)
      for y in url_words:
        quest = quest.replace(y," ")
  cond = []
  for f in found:
    cond.append("url = " + repr(f))
  query = " AND ".join(cond)
  return quest, query

def get_clubs(quest, club_list):
  found=[]
  possible_additions = [" club advisor of "," advisor of ", " advisor for " " club advisor ", "leader of", " club ", " advisor "," advises "," advise "," advising "]
  synonyms = {"Association for Computing Machinery":[" computing machinery club "], "Blockchain at Cal Poly": [" blockchain club "], "Cardistry and Magic":[" cardistry club ", " magic club ", " cardistry and magic club "], "Chinese Christian Fellowship":[" chinese christian club "], "Code The Change":[" code the change club "], "Color Coded":[" color coded club ", " colorcoded ", " colorcoded club "], "Computer Science and Artificial Intelligence":[" artificial intelligence club ", " computer science and artificial intelligence club "],"Computer Science Graduate Student Association":[" graduate student association ", " cs grad student association "], "Critical Global Engagement Club":[" global engagement club "], "CS + Social Good":[" cs and social good club ", " cs and social good ", " cs plus social good club "], "Game Development Club, Cal Poly":[" game development club ", " game developing club "], "Hack4Impact":[" hack for impact club ", " hack for impact "], "Ignite Club":[" ignite "], "Linux Users Group, Cal Poly":[" linix club ", " linix users club ", " linix group "], "Mobile App Development Club":[" app development club ", " mobile app club "], "Roborodentia Club":[" robordentia "], "SLO GLO":[" slo glo club "], "SLO Hacks":[" slo hack ", " slo hacks club "], "White Hat":[" white hat club "],"Women Involved in Software and Hardware":[" women in software club ", " women in hardware club "]}
  for thing in synonyms.keys():
    for club in synonyms[thing]:
      if club.lower() in quest:
        quest = quest.replace(club, " "+ thing+" ")
  for x in club_list:
    if x.lower() in quest: 
      quest = quest.replace(x.lower()," ")
      found.append(x.lower())
      for add in possible_additions:
        quest = quest.replace(add," ")
  cond = []
  for f in found:
    cond.append("LOWER(clubname) = " + repr(f))
  query = " AND ".join(cond)
  return quest, query

def get_research_topics(quest,research_ar):
  found=[]
  research_ar.remove("systems")
  research_ar.append("systems")
  possible_additions = [" researching "," area of study "," study area ", " topic ", " area of interest ", " interested in "," of interest "," research area "]
  for x in research_ar:
    if x in quest: 
      quest = quest.replace(x," ")
      found.append(x)
      for add in possible_additions:
        quest = quest.replace(add," ")
  cond = []
  for f in found:
    cond.append("LOWER(researchinterests) = " + repr(f))
  query = " AND ".join(cond)
  return quest, query
 
def findBuildings(quest):
  cond = ""
  buildings = re.findall(r" building (\d+) ", quest)
  csOther = [" frank e. pilling computer science "," computer science building ", " cs building "]
  for i in csOther: 
    if i in quest:
      buildings.append("14")
  if " jespersen hall " in quest:
    buildings.append("116")
  if " faculty offices east " in quest:
    buildings.append("25")
  if " faculty offices north " in quest:
    buildings.append("47")
  if " poly grove trailer park " in quest:
    buildings.append("92M")
  if len(buildings) != 0:
    for item in buildings: 
      cond += "LOWER(Locations) = "+ repr(item.strip()+"%")+ " AND "
      purge = [" see at building " + item + " ", " talk to in building "+item + " "," in building "+ item + " ", " at building "+ item + " ", " building " + item + " has "," building "]
      for phrase in purge:
        quest = quest.replace(phrase, " ") 
      quest = quest.replace(item, " ")
  return (quest, cond[:-5])

def findEmails(quest):
  cond = ""
  quest = quest.replace("e-mail","email")
  quest = quest.replace(" e mail "," email ")
  emails = re.findall(r" [a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+ ", quest)
  possible_additions = [" email address "," email ", " emails "]
  for email in emails:
    quest = quest.replace(email," ")
  if len(emails) != 0:
    for add in possible_additions:
      quest = quest.replace(add," ")
    for item in emails: 
      cond += "email = " +repr(item.strip()) + " AND "
      purge = [" reach at " + item + " ", " contact at "+ item + " ", " at "+ item+ " ", " email is "+item + " ", " has the email "+item + " ", " "+item + " the email of "]
      for phrase in purge:
        quest = quest.replace(phrase, " ")
      quest = quest.replace(item," ")   
  return (quest, cond[:-5])

def findCourses(quest):
  cond = ""
  possible_additions = [" courses "," classes "," course "," class "]
  courses = re.findall(r" csc\d{3} ", quest)
  courses.extend(re.findall(r" cpe\d{3} ", quest))
  courses.extend(re.findall(r" csc \d{3} ", quest))
  courses.extend(re.findall(r" cpe \d{3} ", quest))
  for course in courses:
    quest = quest.replace(course,"")
  if len(courses) != 0:
    for add in possible_additions:
      quest = quest.replace(add,"")
    for item in courses: 
      cond += "LOWER(Courses) = " + repr(item.strip()) + " AND "
      purge = [" teaching " + item + " ", " teaches " + item + " ", " "+ item + " is taught by "," "+ item + " with "]
      for phrase in purge:
        quest = quest.replace(phrase, " ")
      quest = quest.replace(item," ")
  return (quest, cond[:-5])

def findOffices(quest):
  possible_additions = [" office number "," office "," room "]
  offices = re.findall(r" \d?\d{2}[A-Za-z]?-[A-Za-z0-9]?\d{3}[A-Za-z0-9]? ", quest)
  for off in offices:
    quest = quest.replace(off," ")
  if len(offices) != 0:
    for add in possible_additions:
      quest = quest.replace(add," ")
  cond = []
  for f in offices:
    cond.append("room = " + repr(f))
  query = " OR ".join(cond)
  return quest, query

def findDegreeTypes(quest):
  cond=""
  degrees = []
  phd = [" phd ", " p.h.d ", " ph.d ", "ph.d. ", " grad degree ", " graduate degree ", " postgraduate degree ", " post-graduate degree ", " grad school ", " graduate school ", " postgraduate school ", " post-graduate school "]
  ma= [" m.a ", " master of arts ", " masters ", " master's ", " grad degree ", " graduate degree ", " postgraduate degree ", " post-graduate degree ", " grad school ", " graduate school ", " postgraduate school ", " post-graduate school "]
  ms= [" m.s ", " master of science "," masters ", " master's ", " grad degree ", " graduate degree ", " postgraduate degree ", " post-graduate degree ", " grad school ", " graduate school ", " postgraduate school ", " post-graduate school "]
  bs = [" b.s ", " bs ", " bachelor ", " bachelor of science ", " bachelors ", " bachelor's "," undergrad ", " undergraduate "]
  ba = [" b.a ", " ba ", " bachelor ", " bachelor of arts "," bachelors ", " bachelor's "," undergrad ", " undergraduate "]
  
  if any(a in quest for a in phd):
    degrees.extend(phd)
    cond += "degreetype = 'Ph.D' OR "
  if any(a in quest for a in ma):
    degrees.extend(ma)
    cond += "degreetype = 'M.A' OR "
  if any(a in quest for a in ms):
    degrees.extend(ms)
    cond += "degreetype = 'M.S' OR "
  if any(a in quest for a in bs):
    degrees.extend(bs)
    cond += "degreetype = 'B.S' OR "
  if any(a in quest for a in ba):
    degrees.extend(ba)
    cond += "degreetype = 'B.A' OR "
  if len(degrees) != 0:
    for item in degrees: 
      purge = [" go to " + item + " ", " get their " + item+ " ", " get his "+item+" ", " get her "+ item + " "]
      for phrase in purge:
        quest = quest.replace(phrase, " ")
      quest = quest.replace(item," ")
  if len(cond) > 0:
    cond = "(" + cond[:-4] + ")"
  else:
    cond = ""
  return (quest, cond)

def findCourseNames(quest, courseNames):
  found=[]
  synonyms = {'Fundamentals of Computer Science':[" cs fundamentals ", " computer science fundamentals "], 'Systems Programming':[" systems "], 'Compiler Construction':[" compilers ", " compiler programming ", " compiler building "], 'Music Programming':[" music and programming "], 'Design and  Analysis of Algorithms':[" design and analysis of algorithms ", " algorithms ", " design of algorithms ", " analysis of algorithms "], 'Programming Languages':[" computer languages "], 'Languages and Translators':[" computer langes and translators ", " language translators "], 'Knowledge Discovery from Data':[" knowledge and discovery from data ", " discovery from data ", " knowledge from data "], 'Introduction to Database Systems':[" into to systems ", " intro to databases ", " intro databases "], 'Database Modeling, Design and Implementation':[" database modeling ", " database design ", " database implementation "], 'Database Systems':[" databases ", " data systems "], 'Thesis Seminar':[" thesis class "], 'Introduction to Computer Security':[" intro to security ", " security intro "], 'Introduction to Computing':[" computing intro ", " intro to computing ", " intro computing "], 'Current Topics in Computer Security':[" security ", " computer security ", " current computer security "], 'Professional Responsibilities':[" responsibilities ", " professional responsibility "], 'Computers and Society':[" cs and society ", " the computer and society "], 'Senior Project II':[" senior project 2 "], 'Software Engineering I':[" software engineering 1 ", " software engineering one "], 'Accelerated Introduction to Computer Science':[" accelerated intro to computer science "], 'Data Structures':[" structures "], 'C and Unix':[" c ", " unix "], 'Teaching Computer Science':[" teaching cs "], 'Individual Software Design and Development':[" sofware design and development "], 'Introduction to Object Oriented Design Using Graphical User Interfaces':[" object oriented guis ", " intro to object oriented guis"], 'Human-Computer Interaction Theory and Design':[" human computer interaction theory ", " human computer interaction design ", " human and computer interaction theory "," human and computer interaction design "], 'Selected Advanced Topics':[" advanced topics "], 'Introduction to Computer Graphics':[" intro to graphics "], 'Advanced Rendering Techniques':[" advanced rendering "], 'Computer Architecture':[" cs architecture "], 'Software Construction':[" construction of software "], 'Senior Project - Software Deployment':[" senior project for software"], 'Introduction to Computer Organization':[" computer organization "], 'Artificial Intelligence':[" ai ", " machine intelligence ", "computer intelligence "], 'Introduction to Software Engineering':[" intro to software engineering ", " software engineering introduction "], 'Software Requirements Engineering':[" software requirements ", " engineering requirements "], 'Current Topics in Software Engineering':[" topics in software engineering "], 'Mobile Application Development':[" app development ", " app creation ", " app building ", " mobile apps ", " mobile app "], 'Personal Software Process':[" personal software "], 'Current Topics in Computer Science':[" current computer science "], 'Microcontrollers and Embedded Applications':[" microcontrollers "], 'Implementation of Operating Systems':[" implementing os's ", " implementing an os ", " implementating operating systems "], 'Introduction to Operating Systems':[" intro to os's ", " intro to os ", " intro operating systems ", " intro os "], 'User-Centered Interface Design and Development':[" ui design and development ", " ui design ", "ui development ", " interface design and development", " interface design ", " interface development "], 'Introduction to Interactive Entertainment':[" interactive entertainment "], 'Knowledge Based Systems':[" knowledge systems "], 'Computer Support for Knowledge Management':[" support for knowledge managment "], 'Software Engineering II':[" software engineering 2 ", " software engineering two "], 'Fundamentals of Computer Science I Supplemental Instruction':[" supplement to fundamentals of computer science "], 'Fundamentals of Computer Science for Scientists and Engineers I':[" fundamentals of computer science for scientists and engineers one "], 'Theory of Computation I':[" computation theory one ", " theory of computation one ", " computation  theory 1 ", " theory of computation 1 "], 'Theory of Computation II': [" computation theory two ", " theory of computation two ", " computation  theory 2 ", " theory of computation 2 "], 'Project-Based Object-Oriented Programming and Design': [" object oriented programming projects "], 'Introduction to Computer Networks':[" intro to networks ", " intro to computer networks "], 'Advanced Computer Networks':[" advanced networks "], 'Computer Networks: Research Topics' :[" research topics in networks "], 'Discrete Structures':[" discrete structuring "], 'Special Problems': [" special operations "], 'Operating Systems':[" os ", " os's "], 'Current Topics in Computer Systems':[" current systems "], 'Distributed Computing': [" computation distribution "], 'Computers for Poets':[" computer poetry "], 'Programming for Engineering Students':[" proramming for engineers "], 'Computer Programming for Scientists and Engineers':[" programming for scientists "], 'Database Management Systems Implementation':[" database management ", " implementing database management "], 'Computer Engineering Orientation':[" engineering orientation "], 'Senior Project I':[" senior project 1 ", " senior project one "], 'Introduction to Distributed Computing': [" intro to computation distribution ", " intro to distributed computing "], 'Distributed Systems':[" system distribution "], 'Fundamentals of Computer Science for Scientists and Engineers II':[" fundamentals of cs for scientists two ", " fundamentals of cs for scientists 2 "], 'Cryptography Engineering':[" cryptography "]}
  possible_additions = [" is the professor for ", " is the lecturer for ", " is the instructor for ", " offers a section of ", " offers sections of ", " teaches a section of ", " teaches sections of ", " teaches ", " offers "]
  for thing in synonyms.keys():
    for name in synonyms[thing]:
      if name.lower() in quest:
        quest = quest.replace(name.lower(), " "+ thing+" ")
        found.append(name)
  for x in courseNames:
    if x.lower() in quest: 
      quest = quest.replace(x.lower()," ")
      found.append(x)
      for end in possible_additions:
        quest = quest.replace(end," ")
  cond = []
  for f in found:
    cond.append("LOWER(courseName) = " + repr(f.strip()))
  query = " AND ".join(cond)
  return quest, query

def findPositions(quest):#special case if asking for position of just professor
  cond = ""
  position = []
  total = []
  associateProf = [" associate professor ", " associate professors "]
  if any(a in quest for a in associateProf):
    total.extend(associateProf)
    position.append("Associate Professor")
  lecturer = [" lecturer ", " lecturers "]
  if any(a in quest for a in lecturer):
    total.extend(lecturer)
    position.append("Lecturer")
  assistantProf = [" assistant professor ", " assistant professors "]
  if any(x in quest for x in assistantProf):
    total.extend(assistantProf)
    position.append("Assistant Professor")
  if len(position) != 0:
    for item in position: 
      cond += "Position = " + repr(item) + " OR "
    for i in total:
      purge = [" is an " + i + " ", " is a " + i + " ", " all of the " + i + " "]
      for phrase in purge:
        quest = quest.replace(phrase, " ")
      quest = quest.replace(i," ")
  return (quest, cond[:-4])
    
def findGrades(quest):
  grade = re.findall(r" got an? (A-?|[BCD][+-]?|F$) ", quest)
  grade.extend(re.findall(r" received an? (A-?|[BCD][+-]?|F$) ", quest))
  grade.extend(re.findall(r" an? (A-?|[BCD][+-]?|F$)", quest))
  grade.extend(re.findall(r" grade of (A-?|[BCD][+-]?|F$) ", quest))
  poss_add = [" grade of "," grade "," received "]
  for gr in grade: 
    quest = quest.replace(gr, " ")
  if len(grade) != 0:
    for add in poss_add:
      quest = quest.replace(add," ")
  cond = []
  for f in grade:
    cond.append("grade = " + repr(f))
  query = " AND ".join(cond)
  return quest, query

def findRating(quest): 
  cond =""
  quest = quest.replace(" polyrat"," rat")
  ratings=[]
  greaterEqual = re.findall(r" (rating of at least ([0-3]\.?\d*|4)) ", quest)
  greaterEqual.extend(re.findall(r" (minimum rating of ([0-3]\.?\d*|4)) ", quest))
  greaterEqual.extend(re.findall(r" (rated at least ([0-3]\.?\d*|4)) ", quest))
  greaterEqual.extend(re.findall(r" (rating greater than or equal to ([0-3]\.?\d*|4)) ", quest))
  greaterEqual.extend(re.findall(r" (rating of at least a ([0-3]\.?\d*|4)) ", quest))
  greaterEqual.extend(re.findall(r" (minimum rating of a ([0-3]\.?\d*|4)) ", quest))
  greaterEqual.extend(re.findall(r" (rated at least a ([0-3]\.?\d*|4)) ", quest))
  greaterEqual.extend(re.findall(r" (rating greater than or equal to a ([0-3]\.?\d*|4)) ", quest))
  ratings.extend(greaterEqual)
  for i in greaterEqual: 
    cond+= "polyrating >= " + i[1] + " AND "
  lessEqual = re.findall(r" (rating no more than ([0-3]\.?\d*|4)) ", quest)
  lessEqual.extend(re.findall(r" (rating no greater than ([0-3]\.?\d*|4)) ", quest))
  lessEqual.extend(re.findall(r" (rating no higher than ([0-3]\.?\d*|4)) ", quest))
  lessEqual.extend(re.findall(r" (rated no greater than ([0-3]\.?\d*|4)) ", quest))
  lessEqual.extend(re.findall(r" (rated no higher than ([0-3]\.?\d*|4)) ", quest))
  lessEqual.extend(re.findall(r" (rating less than or equal to ([0-3]\.?\d*|4)) ", quest))
  lessEqual.extend(re.findall(r" (rating no more than a ([0-3]\.?\d*|4)) ", quest))
  lessEqual.extend(re.findall(r" (rating no greater than a ([0-3]\.?\d*|4)) ", quest))
  lessEqual.extend(re.findall(r" (rating no higher than a ([0-3]\.?\d*|4)) ", quest))
  lessEqual.extend(re.findall(r" (rated no greater than a ([0-3]\.?\d*|4)) ", quest))
  lessEqual.extend(re.findall(r" (rated no higher than a ([0-3]\.?\d*|4)) ", quest))
  lessEqual.extend(re.findall(r" (rating less than or equal to a ([0-3]\.?\d*|4)) ", quest))
  ratings.extend(lessEqual)
  for i in lessEqual: 
      cond+= "polyrating <= " + i[1]+ " AND "
  greater = re.findall(r" (rating greater than ([0-3]\.?\d*|4)) ", quest)
  greater.extend(re.findall(r" (rated greater than ([0-3]\.?\d*|4)) ", quest))
  greater.extend(re.findall(r" (rating over ([0-3]\.?\d*|4)) ", quest))
  greater.extend(re.findall(r" (rating higher than ([0-3]\.?\d*|4)) ", quest))
  greater.extend(re.findall(r" (rated higher than ([0-3]\.?\d*|4)) ", quest))
  greater.extend(re.findall(r" (rating more than ([0-3]\.?\d*|4)) ", quest))
  greater.extend(re.findall(r" (rating of more than ([0-3]\.?\d*|4)) ", quest))
  greater.extend(re.findall(r" (rated more than ([0-3]\.?\d*|4)) ", quest))
  greater.extend(re.findall(r" (greater rating than ([0-3]\.?\d*|4)) ", quest))
  greater.extend(re.findall(r" (higher rating than ([0-3]\.?\d*|4)) ", quest))
  greater.extend(re.findall(r" (rating above ([0-3]\.?\d*|4)) ", quest))
  greater.extend(re.findall(r" (rating greater than a ([0-3]\.?\d*|4)) ", quest))
  greater.extend(re.findall(r" (rated greater than a ([0-3]\.?\d*|4)) ", quest))
  greater.extend(re.findall(r" (rating over a ([0-3]\.?\d*|4)) ", quest))
  greater.extend(re.findall(r" (rating higher than a ([0-3]\.?\d*|4)) ", quest))
  greater.extend(re.findall(r" (rated higher than a ([0-3]\.?\d*|4)) ", quest))
  greater.extend(re.findall(r" (rating more than a ([0-3]\.?\d*|4)) ", quest))
  greater.extend(re.findall(r" (rating of more than a ([0-3]\.?\d*|4)) ", quest))
  greater.extend(re.findall(r" (rated more than a ([0-3]\.?\d*|4)) ", quest))
  greater.extend(re.findall(r" (greater rating than a ([0-3]\.?\d*|4)) ", quest))
  greater.extend(re.findall(r" (higher rating than a ([0-3]\.?\d*|4)) ", quest))
  greater.extend(re.findall(r" (rating above a ([0-3]\.?\d*|4)) ", quest))
  ratings.extend(greater)
  for i in greater: 
      cond+= "polyrating > " + i[1] + " AND "
  less = re.findall(r" (rating less than ([0-3]\.?\d*|4)) ", quest)
  less.extend(re.findall(r" (rated less than ([0-3]\.?\d*|4)) ", quest))
  less.extend(re.findall(r" (rating lower than ([0-3]\.?\d*|4)) ", quest))
  less.extend(re.findall(r" (rated lower than ([0-3]\.?\d*|4)) ", quest))
  less.extend(re.findall(r" (rating under ([0-3]\.?\d*|4)) ", quest))
  less.extend(re.findall(r" (rated under ([0-3]\.?\d*|4)) ", quest))
  less.extend(re.findall(r" (lower rating than ([0-3]\.?\d*|4)) ", quest))
  less.extend(re.findall(r" (lesser rating than ([0-3]\.?\d*|4)) ", quest))
  less.extend(re.findall(r" (rating below ([0-3]\.?\d*|4)) ", quest))
  less.extend(re.findall(r" (rating less than a ([0-3]\.?\d*|4)) ", quest))
  less.extend(re.findall(r" (rated less than a ([0-3]\.?\d*|4)) ", quest))
  less.extend(re.findall(r" (rating lower than a ([0-3]\.?\d*|4)) ", quest))
  less.extend(re.findall(r" (rated lower than a ([0-3]\.?\d*|4)) ", quest))
  less.extend(re.findall(r" (rating under a ([0-3]\.?\d*|4)) ", quest))
  less.extend(re.findall(r" (rated under a ([0-3]\.?\d*|4)) ", quest))
  less.extend(re.findall(r" (lower rating than a ([0-3]\.?\d*|4)) ", quest))
  less.extend(re.findall(r" (lesser rating than a ([0-3]\.?\d*|4)) ", quest))
  less.extend(re.findall(r" (rating below a ([0-3]\.?\d*|4)) ", quest))
  ratings.extend(less)
  for i in less:
    cond+= "polyrating < " + i[1] + " AND "
  eq = re.findall(r" (rating equal ([0-3]\.?\d*|4)) ", quest)
  eq.extend(re.findall(r" (rated ([0-3]\.?\d*|4)) ", quest))
  eq.extend(re.findall(r" (rating ([0-3]\.?\d*|4)) ", quest))
  eq.extend(re.findall(r" (rating under ([0-3]\.?\d*|4)) ", quest))
  eq.extend(re.findall(r" (rated at ([0-3]\.?\d*|4)) ", quest))
  eq.extend(re.findall(r" (a rating of ([0-3]\.?\d*|4)) ", quest))
  eq.extend(re.findall(r" (rated at a ([0-3]\.?\d*|4)) ", quest))
  eq.extend(re.findall(r" (rated a ([0-3]\.?\d*|4)) ", quest))
  eq.extend(re.findall(r" (rating equal to a ([0-3]\.?\d*|4)) ", quest))
  eq.extend(re.findall(r" (rating equal to ([0-3]\.?\d*|4)) ", quest))
  eq.extend(re.findall(r" (equal rating of a ([0-3]\.?\d*|4)) ", quest))
  ratings.extend(eq)
  for i in eq:
    cond+= "polyrating = " + i[1] + " AND "
  for item in ratings: 
    quest = quest.replace(item[0],"")
  return(quest, cond[:-5])

def findYear(quest): 
  cond =""
  years = []
  decades = re.findall(r" the (19[0-9]0|20[0-1]0)'?s ",quest)
  if len(decades) != 0:
    for d in decades:
      cond += "Year >= " + repr(d) + " AND Year <= " + repr(str(int(d) + 9)) + " AND "
  year = re.findall(r"\s?(190[1-9]|19[1-9][0-9]|20[0-1][0-9])\s?", quest)
  if len(year)== 1:
    for item in year:
      cond += "Year = " + repr(item) + " AND "
      purge = [" in " + item + " ", " during "+ item + " ", " in the " + item + "s ", " in the " + item + "'s "," during the " + item + "s "," during the " + item + "'s "]
      for phrase in purge:
        quest = quest.replace(phrase, " ")
      quest = quest.replace(item," ")
  elif len(year) == 2:
    bet = "between " + year[0] + " and " + year[1]
    if bet in quest:
      cond += "Year >= " + repr(year[0]) + " AND Year <= " + repr(year[1]) + " AND "
      quest = quest.replace(bet,"")
    elif (year[0] + " or " + year[1]) in quest:
      cond += "(Year = " + repr(year[0]) + " OR Year = " + repr(year[1]) + ") AND "
  elif len(year) > 2:
    cond+="("
    for yr in year:
      cond += "Year = " + repr(yr) + " OR "
    cond+=") AND "
  return (quest, cond[:-5])

def get_start_end(quest):
  cond =""
  years = []
  decades = re.findall(r" the (19[0-9]0|20[0-1]0)'?s ",quest)
  year_words = [" year ", " years ", " decade "]
  if len(decades) != 0:
    for d in decades:
      if " start " in quest or " started " in quest or " began " in quest:
        cond += "startdate>= " + repr(d) + " AND startdate <= " + repr(str(int(d) + 9)) + " AND "
      elif " quit " in quest or " left " in quest or " stopped " in quest:
        cond += "enddate>= " + repr(d) + " AND enddate <= " + repr(str(int(d) + 9)) + " AND "
      else:
        cond += ("((startdate>= " + repr(d) + " AND startdate <= " + repr(str(int(d) + 9)) + ") OR " +
          "(enddate>= " + repr(d) + " AND enddate <= " + repr(str(int(d) + 9)) + ") OR " +
          "(startdate< " + repr(d) + " AND enddate > " + repr(str(int(d) + 9)) + ")) AND ")
      quest = quest.replace(d,"")
    for yr in year_words:
      quest = quest.replace(yr,"")
  year = re.findall(r"\s?(190[1-9]|19[1-9][0-9]|20[0-1][0-9])\s?", quest)
  if len(year)== 1:
    if ("before " + year[0]) in quest:
      if " start " in quest or " started " in quest or " began " in quest:
        cond += "startdate <= " + repr(year[0]) + " AND "
      elif " quit " in quest or " left " in quest or " stopped " in quest:
        cond += "enddate <= " + repr(year[0]) + " AND "
      else:
        cond += "startdate<= " + repr(year[0]) + " AND "
    elif ("after " + year[0]) in quest:
      if " start " in quest or " started " in quest or " began " in quest:
        cond += "startdate >= " + repr(year[0]) + " AND "
      elif " quit " in quest or " left " in quest or " stopped " in quest:
        cond += "enddate >= " + repr(year[0]) + " AND "
      else:
        cond += "enddate >= " + repr(year[0]) + " AND "
    else:
      cond += ("((startdate>= " + repr(year[0]) + " AND startdate <= " + repr(year[0]) + ") OR " +
          "(enddate>= " + repr(year[0]) + " AND enddate <= " + repr(year[0]) + ") OR " +
          "(startdate< " + repr(year[0]) + " AND enddate > " + repr(year[0]) + ")) AND ")
    for phrase in year_words:
      quest = quest.replace(phrase, " ")
    quest = quest.replace(year[0]," ")
  elif len(year) == 2:
    bet = "between " + year[0] + " and " + year[1]
    if bet in quest:
      if " start " in quest or " started " in quest or " began " in quest:
        cond += "startdate>= " + repr(year[0]) + " AND startdate <= " + repr(year[1]) + " AND "
      elif " quit " in quest or " left " in quest or " stopped " in quest:
        cond += "enddate>= " + repr(year[0]) + " AND enddate <= " + repr(year[1]) + " AND "
      else:
        cond += ("((startdate>= " + repr(year[0]) + " AND startdate <= " + repr(year[1]) + ") OR " +
          "(enddate>= " + repr(year[0]) + " AND enddate <= " + repr(year[1]) + ") OR " +
          "(startdate< " + repr(year[0]) + " AND enddate > " + repr(year[1]) + ")) AND ")
      quest = quest.replace(bet,"")
    else:
      if " start " in quest or " started " in quest or " began " in quest:
        cond += "startdate>= " + repr(year[0]) + " OR startdate <= " + repr(year[1]) + " AND "
      elif " quit " in quest or " left " in quest or " stopped " in quest:
        cond += "enddate>= " + repr(year[0]) + " AND enddate <= " + repr(year[1]) + " AND "
      else:
        cond += ("((startdate>= " + repr(year[0]) + " AND startdate <= " + repr(year[1]) + ") OR " +
          "(enddate>= " + repr(year[0]) + " AND enddate <= " + repr(year[1]) + ") OR " +
          "(startdate< " + repr(year[0]) + " AND enddate > " + repr(year[1]) + ")) AND ")
      quest = quest.replace(year[0],"")
      quest = quest.replace(year[1],"")
    for phrase in year_words:
      quest = quest.replace(phrase, " ")
  return (quest, cond[:-5])

def findWeekday(quest):
  cond = ""
  day = []
  found = []
  curWeekday = datetime.datetime.today().weekday()
  date = re.findall(r" office hours on (\d{1,2})\/(\d{1,2})\/(?:\d{2}){1,2}$ ", quest)
  for d in date:
    day.append(datetime.date(d[0][2], d[0][0], d[0][1]).weekday())
  relation = re.findall(r" in (\d+) day ", quest)
  relation.extend(re.findall(r" (\d+) days from now ", quest))
  relation.extend(re.findall(r" (\d+) day from now ", quest))
  found.extend(relation)
  if (re.match(r" tomorrow ",quest)):
    found.append(" tomorrow ")
    day.append((1 + curWeekday)%7)
  for val in relation:
    day.append((val + curWeekday)%7)
  negRelation =re.findall(r" (\d+) days ago ", quest)
  negRelation.extend(re.findall(r" (\d+) day ago ", quest))
  found.extend(negRelation)
  if (re.match(r" day before yesterday ",quest)):
    day.append((-2 + curWeekday)%7)
  elif (re.match(r" yesterday ",quest)):
    day.append((-1 + curWeekday)%7)
    found.append(" yesterday ")
  weekDay = []
  for d in day:
    if d == 0:
      weekDay.append("M")
    elif d == 1:
      weekDay.append("T")
    elif d == 2:
      weekDay.append("W")
    elif d == 3:
      weekDay.append("R")
    elif d== 4:
      weekDay.append("F")
  if re.match(r" monday ",quest):
    weekDay.append("M")
  if re.match(r" tuesday ",quest):
    weekDay.append("T")
  if re.match(r" wednesday ",quest):
    weekDay.append("W")
  if re.match(r" thursday ",quest):
    weekDay.append("R")
  if re.match(r" friday ",quest):
    weekDay.append("F")
  if len(weekDay) != 0:
    for item in weekDay:
      cond += "Days = " + repr(item) + " AND "
      purge = [" on " + item +" ", " next " +item +" ", " last "+item + " ", " day before " +item + " ", " day after "+ item+ " "," "+ item+ " "]
      for phrase in purge:
        quest = quest.replace(phrase, " ")
      quest = quest.replace(item," ")
  return (quest, cond[:-5]) 


def findTime(quest):
  cond = ""
  times = []
  nowTerm = [" right now ", " currently ", " at this moment ", " at the moment ", " now ", " at this instant ", " this instant "]
  timeBefore = re.findall(r" before ((1[012]|[1-9]):?[0-5]?[0-9]?(\\s)?(?i)(am|pm)) ", quest)
  timeBefore.extend(re.findall(r" ((1[012]|[1-9]):?[0-5]?[0-9]?(\\s)?(?i)(am|pm)) or before ", quest))
  if len(timeBefore) != 0:
    times.extend(timeBefore[0])
    for i in timeBefore: 
      t = datetime.datetime.strptime(i[0], '%I%p').strftime('%H:%M:%S')
      cond += "EndTime >= " + repr(t) +" AND "
  timeAfter = re.findall(r" after ((1[012]|[1-9]):?[0-5]?[0-9]?(\\s)?(?i)(am|pm)) ", quest)
  timeAfter.extend(re.findall(r" ((1[012]|[1-9]):?[0-5]?[0-9]?(\\s)?(?i)(am|pm)) or after ", quest))
  if len(timeAfter) != 0:
    times.extend(timeAfter[0])
    for i in timeAfter: 
      t = datetime.datetime.strptime(i[0], '%I%p').strftime('%H:%M:%S')
      cond += "StartTime >= " + repr(t) +" AND "
  timeAt = re.findall(r" at ((1[012]|[1-9]):?[0-5]?[0-9]?(\\s)?(?i)(am|pm)) ", quest)
  if len(timeAt) != 0:
    times.extend(timeAt[0])
    for i in timeAt: 
      t = datetime.datetime.strptime(i[0], '%I%p').strftime('%H:%M:%S')
      t2 = datetime.datetime.strptime( str(int(i[0][-3]) + 1)+i[0][-2:], '%I%p').strftime('%H:%M:%S')
      cond += "StartTime >= " + repr(t)+" AND EndTime <= " + repr(t2)+" AND "
    
  timeBetween = re.findall(r" between ((1[012]|[1-9]):?[0-5]?[0-9]?(\\s)?(?i)(am|pm)) and ((1[012]|[1-9]):?[0-5]?[0-9]?(\\s)?(?i)(am|pm)) ", quest)
  if len(timeBetween) != 0:
    times.extend(timeBetween[0])
    for i in timeBetween: 
      t = datetime.datetime.strptime(i[0][0], '%I%p').strftime('%H:%M:%S')
      t2 = datetime.datetime.strptime( str(int(i[0][-3]) + 1)+i[0][-2:], '%I%p').strftime('%H:%M:%S')
      cond += "StartTime >= " + repr(t) +" AND EndTime <= " + repr(t2)+ " AND "
  if any(now in quest for now in nowTerm):
    cur = datetime.datetime.now()
    curHour = cur.hour
    curTime= datetime.datetime.strptime(str(curHour),'%H').strftime('%H:%M:%S')
    nextHour = (curHour + 1)%25
    curNexthour= datetime.datetime.strptime(str(nextHour),'%H').strftime('%H:%M:%S')
    curYear = cur.year
    quarters = [" Winter ", " Spring ", " Summer "," Fall "]
    if cur.month >=9 and cur.month<=12:
      curQ = 3
    elif cur.month >=1 and cur.month<=3:
      curQ = 0
    elif cur.month >=4 and cur.month<=6:
      curQ = 1
    else:
      curQ = 2
    curDay = cur.weekday()
    if curDay == 0:
      weekday = "%M%"
    elif curDay == 1:
      weekday = "%T%"
    elif curDay == 2:
      weekday = "%W%"
    elif curDay == 3:
      weekday = "%R%"
    elif curDay == 4:
      weekday = "%F%"
    else:
      weekday = "%S%"

    cond += "StartTime >= " + repr(curTime) + " AND EndTime <= " + repr(curNexthour) + " AND Quarter = " + repr(quarters[curQ].strip()) + " AND Year = " + repr(curYear) + " AND Days LIKE " + repr(weekday) + " AND "
  
  if len(times) != 0:
    for time in times:
      for item in time:
        purge = [" at " + item + " ", " before " +item + " ", " after "+item+ " "," "+ item + " or after "," "+ item +" and after "," "+ item + " or later "," "+ item +" and later "," "+ item + " or before "," "+ item +" and before "," "+ item + " or earlier "," "+ item +" and earlier "] #between times?
        for phrase in purge:
          quest = quest.replace(phrase, " ")
  return (quest, cond[:-5])

def get_select(quest, pred, where,colms):
  cols=set()
  quest = " " + quest + " "
  nlp = spacy.load('en')
  doc = nlp(quest)
  i=0
  questw = doc[i]
  question_words=["who","whom","what","why","where","when","how","is","does","do","can","will","would","are","whose","did","has","could","should","which","tell me","answer"]
  while str(questw).lower() not in question_words and i < len(doc) -1:
    i+=1
    questw = doc[i]
  if questw.dep_ == "advmod":
    questw = str(questw) +" " + questw.head.text  
  questw = str(questw)
  if (questw == "how have" or questw == "how are" ) and " how many " in quest:
    questw = "how many"
  noun = ""
  for token in doc:
    # For each noun (possibly verbs e.g. researching?), check with synonyms to match it with a column of the table. 
    # If no match found, do count(*)
    if (token.pos_ == "NOUN" or token.pos_ == "PROPN") and token.text != questw:
      noun = get_word(token,doc,token.text)[2]
  synonyms = {}
  cp=[]
  profRefrence = [" professors ", " professor "]
  studentRefrence = [" students ", " student "]
  polyrating=[" polyratings ", " poly rating ", " poly ratings ", " rated ", " rating ", " rate ", " ratings ", " good ", " bad ", " quality ", "well liked"]
  researchInts = [" research interests ", " research ", " areas of interests ", " research areas ", " areas of interest ", " areas of expertise ", " interested in ", " interests ", " researching ", " researched "]
  journName = [" journal ", " journals "]
  paperName = [" paper ", " papers ", " publication ", " publications ", " written "]
  projName = [" senior projects ", " senior project ", " project ", " projects "]
  startD = [" start ", " begin "]
  endD = [" end ", " stop ", " quit "]
  contact = [" reach ", " get in touch ", " contact ", " get a hold of ", " talk ", " communicate ", " chat ", " get ahold of "]
  email = [" email address ", " email addresses "," email ", " emails"]
  phone = [" call ", " phone ", " phone number ", " phones "]
  officeHr = [ " meet ", " see ", " office hours ", " office open "]
  webSite = [ " website ", " web page ", " webpage ", " personal site ", " homepage ", " web site ", " url "]
  office = [" location ", " located ", " office number ", " office room ", " room number ", " room " ," office ", " location ", " locate ", " find "]
  jobsRef = [" position ", " positions ", " job ", " jobs ", " title ", " titles "]
  univRefrence = [" university ", " college ", " school ", " study ", " studied ", " attend "]
  degTypeRefrence= [" degree ", " level of education "]
  dyear = [" graduate ", " graduated ", " year ", " long ago "]
  clubs = [" name of club ", " club named ", "club ", " clubs ", " advised by ", " advised ", " group "]
  courses = [" course ", " courses ", " class ", " teach ", " taught ", " classes ", " lecture ", " lectures "]
  chairRef = [" department chair ", " chair ", " department head ", " head of the department "]
  courseNameTemp = [" courses ", " classes ", " course ", " class "]
  courseNameRef = [x + "named " for x in courseNameTemp]
  courseNameRef.extend([x + "name " for x in courseNameTemp])
  courseNameRef.extend([x + "called " for x in courseNameTemp])
  flag = True
  if pred == "rating": #--------------------------------------------------------
    for x in polyrating:
      if x in quest:
        cols.add("polyrating")
      quest = quest.replace(x, " polyrating ")
    for p in profRefrence:
      if p in quest:
        cols.add("FirstName,LastName")
      quest = quest.replace(p, " FirstName, LastName ")
    if len(cols) == 0:
      if questw == "who" or "by whom" in quest:
        cols.add("FirstName,LastName")
  elif pred == "research": #----------------------------------------------------
    for x in researchInts:
      if x in quest:
        cols.add("researchinterests")
      quest = quest.replace(x, " researchinterests ")
    for stud in  studentRefrence:
      if stud in quest:
        cols.add("studentname")
      quest = quest.replace(stud, " studentname ")
    for journ in journName:
      if journ in quest:
        cols.add("journalname")
      quest = quest.replace(journ, " journalname ")
    for paper in  paperName:
      if paper in quest:
        cols.add("papername")
      quest = quest.replace(paper, " papername ")
    for p in profRefrence:
      if p in quest:
        cols.add("FirstName,LastName")
      quest = quest.replace(p, " FirstName, LastName ")
    for proj in  projName:
      if proj in quest:
        cols.add("projectname")
      quest = quest.replace(proj, " projectname ")
    if len(cols) == 0:
      if questw == "who" or "by whom" in quest:
        cols.add("FirstName,LastName")
  elif pred == "jobs": #--------------------------------------------------------
    for p in profRefrence:
      if p in quest:
        cols.add("FirstName,LastName")
      quest = quest.replace(p, " FirstName, LastName ")
    for j in jobsRef:
      if j in quest:
        cols.add("position")
      quest = quest.replace(j, " position ")
    for ch in chairRef:
      if ch in quest:
        cols.add("chair")
      quest = quest.replace(ch, " chair ")
    for x in cp:
      quest = quest.replace(x, "")
    if len(cols) == 0:
      if questw == "who" or "by whom" in quest:
        cols.add("FirstName,LastName")
  elif pred == "contact":#------------------------------------------------------
    for p in profRefrence:
      if p in quest:
        cols.add("FirstName,LastName")
      quest = quest.replace(p, " FirstName, LastName ")
    for x in contact:
      if x in quest:
        cols.add("email")
        cols.add("phone")
      quest = quest.replace(x, " email, phone ")
    for x in email:
      if x in quest:
        cols.add("email")
      quest = quest.replace(x, " email ")
    for x in phone:
      if x in quest:
        cols.add("phone")
      quest = quest.replace(x, " phone ")
    #flag = True
    if "where" in questw:
      cols.add("Locations")
    for i in range(len(officeHr)):
      if flag and officeHr[i] in quest:
        flag = False
        if where == "":
          where = " WHERE Types = 'OH'"
        else:
          where += " and Types = 'OH'"
        quest = quest.replace(officeHr[i], " StartTime, EndTime, Locations, Days ")
        cols.add("StartTime,EndTime")
        cols.add("Locations")
        cols.add("Days")
    for x in webSite:
      if x in quest:
        cols.add("url")
      quest = quest.replace(x, " url ")
    for x in office:
      if x in quest:
        cols.add("room")
      quest = quest.replace(x, " room ")
    for x in cp:
      quest = quest.replace(x, "")
    if len(cols) == 0:
      if questw == "who" or questw == "whose" or "by whom" in quest:
        cols.add("FirstName,LastName")
      if "when" in questw:
        cols.add("StartTime,EndTime")
        cols.add("Days")
  elif pred == "history":#------------------------------------------------------
  #Only degree/university information for tenured profs
    for p in profRefrence:
      if p in quest:
        cols.add("FirstName,LastName")
      quest = quest.replace(p, " FirstName, LastName ")
    for univ in univRefrence:
      if univ in quest:
        cols.add("university")
      quest = quest.replace(univ, " university ")
    for degT in  degTypeRefrence:
      if degT in quest:
        cols.add("degreetype")
      quest = quest.replace(degT, " degreetype ")
    for sd in startD:
      if sd in quest:
        cols.add("startdate")
      quest = quest.replace(sd, " startdate ")
    for ed in endD:
      if ed in quest:
        cols.add("enddate")
      quest = quest.replace(ed, " enddate ")
    for x in dyear:
      if x in quest:
        cols.add("enddate")
      quest = quest.replace(x, " enddate ")
    if len(cols) == 0:
      if questw == "who" or "by whom" in quest:
        cols.add("FirstName,LastName")
  elif pred == "clubs":#--------------------------------------------------------
    for p in profRefrence:
      if p in quest:
        cols.add("FirstName,LastName")
      quest = quest.replace(p, " FirstName, LastName ")
    for x in clubs:
      if x in quest:
        cols.add("clubname")
      quest = quest.replace(x, " clubname ")
  else: # pred = courses -------------------------------------------------------
    for p in profRefrence:
      if p in quest:
        cols.add("FirstName,LastName")
      quest = quest.replace(p, " FirstName, LastName ")
    for x in courseNameRef:
      if x in quest:
        cols.add("courseName")
        quest = quest.replace(x, " courseName ")
    for x in courses:
      if x in quest:
        cols.add("Courses")
      quest = quest.replace(x, " Courses ")
    for x in cp:
      quest = quest.replace(x, "")
    if len(cols) == 0:
      if questw == "who" or "by whom" in quest:
        cols.add("FirstName,LastName")
  query = ""
  cols.add("FirstName,LastName")
  cols = [x.strip() for x in cols]
  colms.extend(cols)
  table = get_table(pred, colms)
  if table == "researchinterests" and len(cols)==0 and "what" in questw:
    cols.append("researchinterests")
  tables = {"Schedule":["FirstName,LastName","Courses","courseName", "Sections","Types", "Days", "StartTime,EndTime", "Locations", "Quarter", "Year"],"clubs":["clubname","FirstName,LastName"],"courses":["FirstName,LastName","Courses","averagegrade","courseName"],"degrees":["FirstName,LastName","university","degreetype","startdate","enddate"],"instructors":["FirstName,LastName","position","chair","room","phone","url","email"],"publications":["FirstName,LastName","journalname","papername"],"ratings":["FirstName,LastName","polyrating"],"researchinterests":["FirstName,LastName","researchinterests"],"seniorprojects":["FirstName,LastName","projectname","studentname"],"tenureinformation":["startdate","enddate","FirstName,LastName"]}
  to_del = set()
  for col in cols:
    if col not in tables[table]:
      to_del.add(col)
  for col in to_del:
    cols.remove(col)
  if not flag and table != "Schedule":
    where = where.replace("and Types = 'OH'","").replace("WHERE Types = 'OH'","")
  noun = ",".join(cols)
  if noun != "" and questw not in ["how many", "does", "is", "will","has","do","was","are","did"]:
    query += "SELECT DISTINCT " + noun + " FROM " + table 
  else:
    query += "SELECT COUNT(*) "+ "FROM " + table 
  return query, where, cols

def get_table(pred,cols):
  if pred == "clubs":
    return "clubs"
  if pred == "rating":
    return "ratings"
  if pred == "jobs":
    return "instructors"
  if pred == "research":
    if "studentname" in cols or "projectname" in cols:
      return "seniorprojects"
    if "journalname" in cols or "papername" in cols:
      return "publications"
    return "researchinterests"
  if pred == "contact":
    if "room" in cols or "phone" in cols or "email" in cols or "url" in cols or "position" in cols:
      return "instructors"
    return "Schedule"
  if pred == "history":
    if "university" in cols or "degreetype" in cols:
      return "degrees"
    return "tenureinformation"
  if pred == "courses":
    if "averagegrade" in cols:
      return "courses"
    return "Schedule"

def gen_query(quest, pred,prof_names,prof_name, research_ar,room_list,univ,urls,students,clubs,courseNames):
  quest = quest.replace(","," ")
  to_remove = ["?","'s","'",'’s', "\"", ";","\n","!",";","/"]
  possible_names = get_possible_names(quest)
  colms = []
  quest = quest.lower()
  for y in to_remove:
    quest = quest.replace(y,"")
  quest = " " + quest + " "
  conds=[]
  quest, names_2, variables = get_names(quest,prof_names,prof_name)
  if len(variables) > 0:
    conds.append(variables)
    colms.append("FirstName,LastName")
    variables=""
  if len(variables) > 0:
    conds.append(variables)
    variables=""
  for nam in names_2:
    for n in possible_names:
      if n.lower() == nam:
        possible_names.remove(n)
  if pred == "rating":#---------------------------------------------------------
    quest, variables = findRating(quest)
    if len(variables) > 0:
      conds.append(variables)
      variables=""
  elif pred == "research": #----------------------------------------------------
    quest, variables = get_journals(quest)
    if len(variables) > 0:
      conds.append(variables)
      colms.append("journalname")
      variables=""
    quest, variables =get_research_topics(quest,research_ar)
    if len(variables) > 0:
      conds.append(variables)
      colms.append("researchinterests")
      variables=""
    quest, variables = get_papers(quest)
    if len(variables) > 0:
      conds.append(variables)
      colms.append("papername")
      variables=""
    quest, names_2, variables = get_student_names(quest,students)
    if len(variables) > 0:
      colms.append("studentname")
      conds.append(variables)
      variables=""
    for nam in names_2:
      for n in possible_names:
        if n.lower() == nam:
          possible_names.remove(n)
    quest, variables = get_senior_proj(quest)
    if len(variables) > 0:
      conds.append(variables)
      colms.append("projectname")
      variables=""
  elif pred == "jobs": #--------------------------------------------------------
    quest, variables = findPositions(quest)
    if len(variables) > 0:
      conds.append(variables)
      variables=""
    if len(possible_names)>0:
      for nam in possible_names:
        quest.replace(nam.lower(),"")
        nrb = HumanName(nam)
        fn = nrb.first.lower()
        ln = nrb.last.lower()
        conds.append("LOWER(FirstName) = " + repr(fn) + " and LOWER(LastName) = " + repr(ln))
  elif pred == "contact": #------------------------------------------------------
    quest, variables = get_phone_numbers(quest)
    if len(variables) > 0:
      conds.append(variables)
      colms.append("phone")
      variables=""
    quest, variables = get_room_numbers(quest,room_list)
    if len(variables) > 0:
      conds.append(variables)
      colms.append("Locations")
      variables=""
    quest, variables = get_url(quest,urls)
    if len(variables) > 0:
      conds.append(variables)
      colms.append("url")
      variables=""
    quest, variables = findBuildings(quest)
    if len(variables) > 0:
      conds.append(variables)
      colms.append("Locations")
      variables=""
    quest, variables = findEmails(quest)
    if len(variables) > 0:
      conds.append(variables)
      colms.append("email")
      variables=""
    quest, variables = findOffices(quest)
    if len(variables) > 0:
      conds.append(variables)
      colms.append("room")
      variables=""
    quest, variables = findTime(quest)
    if len(variables) > 0:
      conds.append(variables)
      colms.append("StartTime")
      colms.append("EndTime")
      variables=""
    quest, variables = findWeekday(quest)
    if len(variables) > 0:
      conds.append(variables)
      colms.append("Days")
      variables=""
  elif pred == "history": #-----------------------------------------------------
    quest, variables = get_university(quest,univ)
    if len(variables) > 0:
      conds.append(variables)
      colms.append("university")
      variables=""
    quest, variables = findDegreeTypes(quest)
    if len(variables) > 0:
      conds.append(variables)
      colms.append("degreetype")
      variables=""
    quest, variables = get_start_end(quest)
    if len(variables) > 0:
      conds.append(variables)
      colms.append("start_date,end_date")
      variables=""
    if len(possible_names)>0:
      for nam in possible_names:
        quest.replace(nam.lower(),"")
        nrb = HumanName(nam)
        fn = nrb.first.lower()
        ln = nrb.last.lower()
        conds.append("LOWER(FirstName) = " + repr(fn) + " and LOWER(LastName) = " + repr(ln))
  # courses :): ----------------------------------------------------------------
  else:
    quest, variables = findCourses(quest)
    if " this quarter " in quest:
      quest = quest.replace(" this quarter ", " in spring 2019 ")
    if " next quarter " in quest:
      quest = quest.replace(" next quarter ", " in summer 2019 ")
    if " last quarter " in quest:
      quest = quest.replace(" last quarter ", " in winter 2019 ")
    if len(variables) > 0:
      conds.append(variables)
      colms.append("Courses")
      variables=""
    quest, variables = findCourseNames(quest, courseNames)
    if len(variables) > 0:
      conds.append(variables)
      colms.append("courseName")
      variables=""
    quest, variables = findWeekday(quest)
    if len(variables) > 0:
      conds.append(variables)
      colms.append("Days")
      variables=""
    quest, variables = findTime(quest)
    if len(variables) > 0:
      conds.append(variables)
      colms.append("StartTime")
      colms.append("EndTime")
      variables=""
    quest, variables = findQuarter(quest)
    if len(variables) > 0:
      conds.append(variables)
      colms.append("Quarter")
      variables=""
    quest, variables = findYear(quest)
    if len(variables) > 0:
      conds.append(variables)
      colms.append("Year")
      variables=""
  query = ""
  if len(conds)>0:
    query += " WHERE " + " AND ".join(conds)
  select, query, cols = get_select(quest, pred, query, colms)
  final_query = select + query
  return final_query

def retrieve_sql_info():
  names_list = []
  name_list = []
  research_ar = []
  room_list = []
  univ = []
  urls=[]
  students = []
  clubs = []
  connection = pymysql.connect(host='localhost', user='sverkruy466',
    password='sverkruydb466', db='sverkruy466', charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)
  with connection.cursor() as cursor:
    sql = "SELECT FirstName, LastName FROM `instructors`"
    cursor.execute(sql)
    result = cursor.fetchall()
    names_list = [x["FirstName"].lower() + " " + x["LastName"].lower() for x in result]
    name_list = [x["LastName"].lower() for x in result]
    sql = "SELECT researchinterests FROM `researchinterests`"
    cursor.execute(sql)
    result = cursor.fetchall()
    research_ar = [x["researchinterests"].lower() for x in result]
    sql = "SELECT DISTINCT Locations FROM `Schedule`"
    cursor.execute(sql)
    result = cursor.fetchall()
    room_list = [x["Locations"].lower() for x in result]
    sql = "SELECT DISTINCT university FROM `degrees`"
    cursor.execute(sql)
    result = cursor.fetchall()
    univ = [x["university"].lower() for x in result]
    sql = "SELECT url FROM `instructors`"
    cursor.execute(sql)
    result = cursor.fetchall()
    urls = [x["url"] for x in result if x["url"] != None and x["url"] != ""]
    sql = "SELECT studentname FROM `seniorprojects`"
    cursor.execute(sql)
    result = cursor.fetchall()
    students = [x["studentname"].lower() for x in result]
    sql = "SELECT clubname FROM `clubs`"
    cursor.execute(sql)
    result = cursor.fetchall()
    clubs = [x["clubname"].lower() for x in result]
    sql = "SELECT DISTINCT Courses FROM `courses`"
    cursor.execute(sql)
    result = cursor.fetchall()
    courseCodes = [x["Courses"] for x in result]
    add = []
    for course in courseCodes:
      add.append(course.replace(" ",""))
    courseCodes.extend(add)
    sql = "SELECT DISTINCT courseName FROM `courses`"
    cursor.execute(sql)
    result = cursor.fetchall()
    courseNames = [x["courseName"].lower() for x in result if x["courseName"] != None]
  return names_list, name_list,research_ar,room_list,univ,urls,students,clubs,courseCodes,courseNames


def moreInfo(quest, pred):
  conf = input("To clarify, you are asking a question relating to " + pred+ " correct?").lower()
  tryAgain = False
  for no in wn.synsets("no").lemma_names():
    if conf == no.lower():
      tryAgain = True
      newTopic = input("Ok, I'm sorry I misunderstood. Which of the following is your question in relation to (please select one): contacting a professor, courses of a professor, professor reserach and work, rating of a professor, history of a professor, clubs of a professor, or faculty positions of a professor").lower()
      if (re.match(r"contact",newTopic)):
        topic = "contact"
      elif (re.match(r"courses",newTopic)):
        topic = "courses"
      elif (re.match(r"research",newTopic)):
        topic = "research"
      elif (re.match(r"rating",newTopic)):
        topic = "rating"
      elif (re.match(r"history",newTopic)):
        topic = "history"
      elif (re.match(r"clubs",newTopic)):
        topic = "clubs"
      elif (re.match(r"jobs",newTopic)):
        topic ="jobs"
      else: 
        tryAgain = False
        topic = ""
        print("Sorry, that does not match one of the categories I asked about, I cannot answer questions which are not about any of these topics.")
        return (tryAgain, topic)
  for yes in wn.synsets("yes").lemma_names():
    if conf == yes.lower():
      print("Oh, well in that case I'm sorry, I just don't know the answer to your question.")
  topic = ""
  print("I am sorry, but I don't know what the answer to your question is.")
  print("You can choose to rephrase")
  return (tryAgain, topic)

def main():
  model_file1 = open("topic_pred.pkl","rb")
  model1 = pickle.load(model_file1)
  model_file1.close()
  
  model_file2 = open("tfidf_topic.pkl","rb")
  tfidf = pickle.load(model_file2)
  model_file2.close()
  
  model_file3 = open("scaling_topic.pkl","rb")
  scaling = pickle.load(model_file3)
  model_file3.close()
  
  model_file4 = open("pca_topic.pkl","rb")
  pca = pickle.load(model_file4)
  model_file4.close()
  
  model_file5 = open("mainMod.pkl","rb")
  model2 = pickle.load(model_file5)
  model_file5.close()

  
  prof_names, prof_name, research_ar,room_list,univ,urls,students,clubs,courseCodes,courseNames = retrieve_sql_info()
  exitStatements = [" leave me alone ", " peace out ", " see ya ", " later girl ", " i'm out of here ", " i'm outta here ", " shut up ", " go away ", " kick rocks ", " goodbye ", " bye ", " smell ya later "," see ya later ", " see you later ", " i want to leave ", " exit ", " quit ", " leave "]
  
  question = ""
  ask =True
  
  while ask:
    sql = ""
    question = input("What would you like to know? ")
    questionMod = " " + question.lower().replace("?","") + " "
    
    if questionMod.replace("!","").replace(" stacia ", " ") in exitStatements:
      ask = False
      break
    
    new = getFeatures(question,research_ar,clubs,univ, courseCodes, courseNames, room_list)
    newIn = pd.DataFrame({"clubs":0, "contact":0, "courses":0, "history":0, "jobs":0, "notOurs":0, "rating":0, "research":0, "research_area":0}, index=[0])

    for n in new.keys():
      newIn[n] = new[n]
    pred = model2.predict(newIn)[0].lstrip()
    
    teachings = [" teaches ", " lectures ", " teachers ", " lecturers ", " teach "]
    actions = [" research ", " researches ", " researching ", " interested ", " has interest ", " studies ", " study ", " studied ", " field ", " specialized ", " specializes "]
    sureOurs = False
    if any(name in questionMod for name in prof_name) or any(n in questionMod for n in prof_names) or any(t in questionMod for t in teachings) or any(r in questionMod for r in actions):
      sureOurs = True
    
    statWords = [" statistics ", " statistic ", " stats ", " stat "]
    if (pred == "notours" or newIn["notOurs"][0]==1 or any(s in questionMod for s in statWords)) and not sureOurs:
      step1 = tfidf.transform([question])
      step2 = scaling.transform(step1.todense())
      step3 = pca.transform(step2)
      pred = model1.predict(step3)
      print("Your best bet MIGHT be to ask the", pred[0].replace("\n", ""), "group, DUDE!")
      pass
    else:
      #special cases 
      contactWords = [" available ", " free to ", " availabity ", " meet with "]
      if sureOurs and any(word in questionMod for word in contactWords):
        pred = "contact"
        sql = gen_query(question, pred,prof_names,prof_name, research_ar,room_list,univ,urls,students,clubs,courseNames)
      elif sureOurs and any(t in questionMod for t in teachings):
        pred = "courses"
        sql = gen_query(question, pred,prof_names,prof_name, research_ar,room_list,univ,urls,students,clubs,courseNames)
      elif sureOurs and any(r in questionMod for r in actions):
        pred = "research"
        sql = gen_query(question, pred,prof_names,prof_name, research_ar,room_list,univ,urls,students,clubs,courseNames)
      elif pred != "notours":
        sql = gen_query(question, pred,prof_names,prof_name, research_ar,room_list,univ,urls,students,clubs,courseNames)
      connection = pymysql.connect(host='localhost', user='sverkruy466',password='sverkruydb466', db='sverkruy466', charset='utf8mb4',cursorclass=pymysql.cursors.DictCursor)
      with connection.cursor() as cursor:
        try:
          cursor.execute(sql)
          result = cursor.fetchall()
          resultToEnglish(question, sql, result)
          print()
        except:
          print("Sorry, I'm not sure.")
    #step1 = tfidf.transform([question])
    #step2 = scaling.transform(step1.todense())
    #step3 = pca.transform(step2)
  print("L8R dude, StaCIA out!")
if __name__ == "__main__":
  main()