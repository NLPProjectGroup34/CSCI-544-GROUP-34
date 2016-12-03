from __future__ import division
from collections import Counter
import string
import math
import os
import sys
import numpy as np
from numpy import zeros
from numpy.linalg import svd
from math import log
from math import sqrt
from nltk.corpus import wordnet as wn
from nltk.tokenize import word_tokenize
import nltk
import itertools
import os
import glob
import collections
import datetime
from nltk.corpus import brown
import pandas as pd
import sklearn
import json


training_data = []
def correct_answers(file_path):
    answers_dict = {}
    model_answers = open(file_path,"r").readlines()
    for line in model_answers:
        id = line.split(" ")[0]
        model_answer = (line.replace(id,"")).lower()
        sentence = model_answer.replace("<stop>","").replace(".","").replace(",","").replace("\n","")
        answers_dict[id] = sentence
        training_data.append(sentence)

    return (answers_dict)

prof_ans = correct_answers(r'/Users/shwetha/Desktop/NLP_PROJECT/ShortAnswerGrading_v2.0/data/sent/answers')


all_student_answers = {}
for root, directories, files in os.walk(r'/Users/shwetha/Desktop/NLP_PROJECT/ShortAnswerGrading_v2.0'):
    for directory in directories:
        if directory == "sent":
                path = os.path.join(root, directory)
                for file in glob.glob(os.path.join(path, '[0-9]*')):
                    i =0
                    student_answers = open(file, "r").readlines()
                    for line in student_answers:
                        i = i+ 1
                        id = line.split(" ")[0]
                        student_answer = (line.replace(id,"")).lower()
                        stud_sentence =student_answer.replace("<stop>", "").replace(".", "").replace(",", "").replace("\n","")
                        all_student_answers[id + "." + str(i)]= stud_sentence
                        training_data.append(stud_sentence)

scores_given_by_professor = {}
for root, directories, files in os.walk(r'/Users/shwetha/Desktop/NLP_PROJECT/ShortAnswerGrading_v2.0/data/scores'):
    for directory in directories:
        path = os.path.join(root, directory)
        for file in glob.glob(os.path.join(path, 'ave')):
            x = 0
            student_scores_by_professor = open(file, "r").readlines()
            for line in student_scores_by_professor:
                x = x + 1
                line = line.replace("\n", "")
                scores_given_by_professor[str(directory) + "." + str(x)] = line


# read dictionary from file word_doc
word_doc = dict()

word_doc = json.load(open("/Users/shwetha/Desktop/NLP_PROJECT/LSA_trained_data/word_doc.txt"))
#print(word_doc)

vocabulary = []
#read vocabulary
with open(r"/Users/shwetha/Desktop/NLP_PROJECT/LSA_trained_data/vocabulary.txt","r")as voc:
    vocab= voc.readlines()
    for v in vocab:
        v = v.replace("\n","")
        vocabulary.append(v)
#print(vocabulary)

with open("/Users/shwetha/Desktop/NLP_PROJECT/LSA_trained_data/doclength.txt","r") as doclen:
    mydoc= doclen.read()
#print(type(mydoclist))

mydoclist = int(mydoc)
#print(type(mydoclist))

doc_term_matrix_tfidf_l2 = np.loadtxt("/Users/shwetha/Desktop/NLP_PROJECT/LSA_trained_data/matrix.txt")


def cosine_similarity(vec1=[], vec2=[]):
    nm = 0
    dnm1 = 0
    dnm2 = 0
    for c in range(0, len(vec1)):
        nm += (vec1[c] * vec2[c])
        dnm1 += (vec1[c] ** 2)
        dnm2 += (vec2[c] ** 2)
    dnm1 = sqrt(dnm1)
    dnm2 = sqrt(dnm2)
    dnm = dnm1 * dnm2
    return (nm / dnm)


def calculate_maxSim(word=[], text={}):
    maxSim = 0.0
    for tword in text:
        sim = cosine_similarity(word, text[tword])
        if sim > maxSim:
            maxSim = sim
    return maxSim

def calculate_semantic_similarity(docListLength, uniqueVocabulary=[], str1=[], str2=[]):#list of words of 2 sentences str1, str2
    doc_term_matrix_tfidf_transpose = zip(*doc_term_matrix_tfidf_l2)
    #dictionary of word: tfidf value for each word in str1 str1_vec = {}
    str1_vec = {}
    # dictionary of word: tfidf value for each word in str1 str2_vec = {}
    str2_vec = {}
    #doc_term_matrix_tfidf_transpose = zip(*doc_term_matrix_tfidf_l2)

    for word in str1:
        if (word in uniqueVocabulary):
            str1_vec[word] = doc_term_matrix_tfidf_transpose[uniqueVocabulary.index(word)]
    for word in str2:
        if (word in uniqueVocabulary):
            str2_vec[word] = doc_term_matrix_tfidf_transpose[uniqueVocabulary.index(word)]

    #dictionary of word :idf value for every word in vocabulary
    idf = {}
    for word in word_doc:
        idf[word] = log(float(docListLength) / word_doc[word])

    maxSim1 = 0.0
    maxSim2 = 0.0
    idfSum1 = 0.0
    idfSum2 = 0.0


    for word in str1:

        if (word in uniqueVocabulary):
            maxSim1 += (calculate_maxSim(str1_vec[word], str2_vec) * idf[word])
            idfSum1 += idf[word]
        else:
            maxSim1 += 0
            idfSum1 += 0

    for word in str2:
        if (word in uniqueVocabulary):
            maxSim2 += (calculate_maxSim(str2_vec[word], str1_vec) * idf[word])
            idfSum2 += idf[word]
        else:
            maxSim1 += 0
            idfSum1 += 0

    if (idfSum1 != 0):
        c1 = maxSim1 / idfSum1
    else:
        c1 = 0.0

    if (idfSum2 != 0):
        c2 = maxSim2 / idfSum2
    else:
        c2 = 0.0


    similarity = 0.5 * (c1 + c2)
    return similarity

scores_from_lsa = {}
for prof_key,prof_value in prof_ans.iteritems():
    f1 = open(r'/Users/shwetha/Desktop/NLP_PROJECT/myscores/'+ prof_key+ ".txt","w")
    student_answers_diction = {}
    for stud_key,stud_value in all_student_answers.iteritems():
        if stud_key.startswith(prof_key):
            student_answers_diction[stud_key] = stud_value
    student_answers_dictionary_sorted = collections.OrderedDict(sorted(student_answers_diction.items()))
    for stud_key_for_one_question,stud_value_for_one_question in student_answers_dictionary_sorted.iteritems():
        sem_sim1 = calculate_semantic_similarity(mydoclist, vocabulary, prof_value.split(), stud_value_for_one_question.split())
        print(prof_key)
        print(stud_key_for_one_question)
        print("sim value" + str(sem_sim1))
        f1.write(stud_key_for_one_question + " : " + str(sem_sim1)+ "\n")
    f1.close()

