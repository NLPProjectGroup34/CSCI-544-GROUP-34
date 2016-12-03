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
import codecs
import os
import glob
import collections
import datetime
from nltk.corpus import brown
import nltk
import json
import pandas as pd
from sklearn import datasets, linear_model


#code to calculate accurcy can be done later

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

#print(len(scores_given_by_professor))


def create_dic_of_lsa_scores(file_path):
    scores_given_by_lsa_1 = {}
    for root, directories, files in os.walk(file_path):
        #print(root)
        for directory in directories:
            if (directory=="myscores"):
                path = os.path.join(root, directory)
                #print(path)
                for file in glob.glob(os.path.join(path, "*.txt")):
                    #print(file)
                    student_scores_by_lsa = open(file, "r").readlines()
                    for line in student_scores_by_lsa:
                        ans = line.split(":")
                        score_key = ans[0]
                        score_key = score_key.rstrip()
                        #print(score_key)
                        #print(type(score_key))
                        score_value = ans[1].replace("\n","").lstrip()
                        #print(type(score_value))
                        scores_given_by_lsa_1[score_key]= score_value
    return(scores_given_by_lsa_1)

scores_given_by_lsa = create_dic_of_lsa_scores(r'/Users/shwetha/Desktop/NLP_PROJECT/')

scores_scale = {}

for key in scores_given_by_lsa.keys():
    sem_sim1 = scores_given_by_lsa[key]
    sem_sim1 = float(sem_sim1)
    if sem_sim1 >= 0.8 and sem_sim1 <= 1:
        score = 5
    elif sem_sim1 >= 0.7 and sem_sim1 < 0.8:
        score = 4.5
    elif sem_sim1 >= 0.5 and sem_sim1 < 0.7:
        score = 4
    elif sem_sim1 >= 0.4 and sem_sim1 < 0.5:
        score = 3.5
    elif sem_sim1 >= 0.3 and sem_sim1 < 0.4:
        score = 3
    elif sem_sim1 >= 0.2 and sem_sim1 < 0.3:
        score = 2.5
    elif sem_sim1 >= 0.1 and sem_sim1 < 0.2:
        score = 2

    elif sem_sim1 >= 0.05 and sem_sim1 < 0.1:
        score = 1

    elif sem_sim1 >= 0.0 and sem_sim1 < 0.05:
        score = 0.5
    else:
        score = 0

    scores_scale[key] = score


#print(scores_scale)


def calculate_accuracy(scores_given_by_professor, scores_scale):
    accuracy_count = 0
    for prof_score_key in scores_given_by_professor.keys():
        p_s = scores_given_by_professor[prof_score_key]
        p_s = float(p_s)
        m_s = scores_scale[prof_score_key]
        m_s = float(m_s)
        if (float(m_s) >= (float(p_s) -1.0)) and (float(m_s) <= (float(p_s) +1.0)):
            accuracy_count += 1
    return(accuracy_count)
result = calculate_accuracy(scores_given_by_professor,scores_scale)

final_accuracy = ((result/len(scores_given_by_lsa))*100)


f1_score = (2*precision*recall/(precision+recall))

print("accuracy = " + str(final_accuracy))
