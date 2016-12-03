import os
import glob
import nltk
import csv
import numpy
from numpy.random import normal
from collections import Counter
from math import log
from math import ceil
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import wordnet_ic
brown_ic = wordnet_ic.ic('ic-brown.dat')

student_answers = {}
model_answers = {}
scores = {}
semantic_scores = {}
predicted_scores =  {}
idf = {}
s_ans = {}
m_ans = {}
answers_keys = []

# -------------------------------------- GET STUDENT ANSWERS ------------------------------------
for root, directories, files in os.walk("C:\\Users\\Hariprabha\\Desktop\\NLPProject\\ShortAnswerGrading_v2.0"):
    for directory in directories:
        if directory == "sent":
                path = os.path.join(root, directory)
                for file in glob.glob(os.path.join(path, '[0-9]*')):
                    key = file.replace((path+"\\"), "")
                    value = open(file, "r").readlines()
                    for i in range(0, len(value)):
                        student_answers[key+"."+str(i)] = value[i]

# --------------------------------------- GET MODEL ANSWERS ---------------------------------------
for root, directories, files in os.walk("C:\\Users\\Hariprabha\\Desktop\\NLPProject\\ShortAnswerGrading_v2.0"):
    for directory in directories:
        if directory == "sent":
                path = os.path.join(root, directory)
                for file in glob.glob(os.path.join(path, 'answers')):
                    value = open(file, "r").readlines()
                    for i in range(0, len(value)):
                        temp = value[i].split()
                        key = temp[0]
                        temp = " ".join(temp)
                        model_answers[key] = temp

# --------------------------------------- GET SCORES ---------------------------------------------------
for root, directories, files in os.walk("C:\\Users\\Hariprabha\\Desktop\\NLPProject\\ShortAnswerGrading_v2.0\\data\\scores"):
    for directory in directories:
        key = directory
        ave = []
        me = []
        other = []
        path = os.path.join(root, directory)
        for file in glob.glob(os.path.join(path, '*')):
            text = open(file, "r").read().split()
            text = map(float, text)
            if "ave" in file:
                ave = text
            if "me" in file:
                me = text
            if "other" in file:
                other = text
        for i in range(0, len(ave)):
            scores[key+"."+str(i)] = []
            scores[key+"."+str(i)].append(ave[i])
            scores[key+"."+str(i)].append(me[i])
            scores[key+"."+str(i)].append(other[i])

# ------------------------------------------ TEXT PRE-PROCESSING  ---------------------------------------
def text_preprocessing(dct = {}):
    tmp_dct = {}
    for key in dct:
        tmp = dct[key].replace("<STOP>", "").replace(".", "").replace(",", "").strip("\n").lower().split()
        del tmp[0]
        tmp_lst = []
        for element in tmp:
            if element not in stopwords.words('english'):
                tmp_lst.append(element)
        tmp_dct[key] = tmp_lst
    return tmp_dct

student_answers = text_preprocessing(student_answers)
model_answers = text_preprocessing(model_answers)

# ------------------------------------ PARTS OF SPEECH TAGGING & LEMMATIZATION  ---------------------------------
def pos_tagging(dct = {}):
    tmp_dct = {}
    for key in dct:
        tmp_lst = []
        tmp_lst = nltk.pos_tag(dct[key])
        tmp_dct[key] = [list(element) for element in tmp_lst]
    return tmp_dct

student_answers = pos_tagging(student_answers)
model_answers = pos_tagging(model_answers)

def filter_nvra(dct = {}):
    tmp_dct = {}
    for key in dct:
        tmp_lst = []
        for element in dct[key]:
            if element[1].startswith(('N', 'V', 'J', 'R')):
                tmp_lst.append(element)
        tmp_dct[key] = tmp_lst
    return tmp_dct

student_answers = filter_nvra(student_answers)
model_answers = filter_nvra(model_answers)

def lemmatization(dct = {}):
    tmp_dct = {}
    lemma = WordNetLemmatizer()
    for key in dct:
        tmp_lst = []
        for element in dct[key]:
            pos = ""
            if element[1].startswith('N'):
                pos = "n"
            if element[1].startswith('V'):
                pos = "v"
            if element[1].startswith('J'):
                pos = "a"
            if element[1].startswith('R'):
                pos = "r"
            tmp_elm = [str(lemma.lemmatize(element[0], pos)), pos]
            tmp_lst.append(tmp_elm)
        tmp_dct[key] = tmp_lst
    return tmp_dct

student_answers = lemmatization(student_answers)
model_answers = lemmatization(model_answers)

def word_class_set(dct = {}):
    tmp_dct = {}
    for key in dct:
        tmp_dct[key] = []
        n = []
        v = []
        r = []
        a = []
        for element in dct[key]:
            if element[1] == "n":
                n.append(element[0])
            elif element[1] == "v":
                v.append(element[0])
            elif element[1] == "r":
                r.append(element[0])
            else:
                a.append(element[0])
        tmp_dct[key].append(n)
        tmp_dct[key].append(v)
        tmp_dct[key].append(r)
        tmp_dct[key].append(a)
    return tmp_dct

model_answers = word_class_set(model_answers)
student_answers = word_class_set(student_answers)

# --------------------------------------------- CALCULATE IDF --------------------------------------------------
for key in model_answers:
    tmp_lst = []
    for word_class in model_answers[key]:
        for word in word_class:
            tmp_lst.append(word)
    m_ans[key] = tmp_lst

for key in student_answers:
    tmp_lst = []
    for word_class in student_answers[key]:
        for word in word_class:
            tmp_lst.append(word)
    s_ans[key] = tmp_lst

def calculate_idf(m_ans = {}, s_ans = {}):
    tmp_dct = {}
    idf_tmp = {}
    for key in m_ans:
        tmp_lst = []
        for word in m_ans[key]:
            tmp_lst.append(word)
        tmp_dct[key] = list(set(tmp_lst))
    for key in s_ans:
        td_key = key[0:key.rfind('.')]
        for word in s_ans[key]:
                if word not in tmp_dct[td_key]:
                        tmp_dct[td_key].append(word)

    for key in tmp_dct:
        idf_tmp[key] = []
        no_of_ans = 1.0
        s_ans_tmp = []
        for s_key in s_ans:
            if s_key[0:s_key.rfind('.')] == key:
                s_ans_tmp.append(s_ans[s_key])
        no_of_ans += len(s_ans_tmp)
        for word in tmp_dct[key]:
            count = 0
            if word in m_ans[key]:
                count += 1
            for ans in s_ans_tmp:
                if word in ans:
                    count += 1
            idf_val = log(no_of_ans/count)
            idf_tmp[key].append([word, idf_val])
    return idf_tmp

idf = calculate_idf(m_ans, s_ans)

# ------------------------------------------ WORDNET WORD SIMILARITY SCORE --------------------------------------

def word_similarity(measure, word1, word2, pos):
    wsim = 0.0
    if pos is "n" or pos is "v":
        if pos is "n":
            word1 = wn.synsets(word1, wn.NOUN)
            word2 = wn.synsets(word2, wn.NOUN)
        else:
            word1 = wn.synsets(word1, wn.VERB)
            word2 = wn.synsets(word2, wn.VERB)

        if word1 != [] and word2 != []:
            word1 = word1[0]
            word2 = word2[0]
            if measure == "path":
                wsim = wn.path_similarity(word1, word2)
            if measure == "lch":
                wsim = wn.lch_similarity(word1, word2)
                wsim = (wsim / 3.63758615973)
            if measure == "wup":
                wsim = wn.wup_similarity(word1, word2)
            if measure == "res":
                wsim = word1.res_similarity(word2, brown_ic)
                wsim = wsim / 9.00601439892
            if measure == "jcn":
                wsim = word1.jcn_similarity(word2, brown_ic)
                wsim = wsim / (1e+300)
            if measure == "lin":
                wsim = word1.lin_similarity(word2, brown_ic)
            return wsim
        else:
            return wsim
    else:
        if pos is "r" or pos is "a":
            if word1 is word2:
                return 1.0
            else:
                return 0.0

'''
def word_similarity(measure, word1, word2, pos):
    if word1 is word2:
            wsim = 1.0
    else:
        word1 = word1+"#"+pos+"#1"
        word2 = word2+"#"+pos+"#1"
        if measure in ["path", "wup", "res","lch", "lin", "jcn"]:
            if pos in ["n", "v"]:

                pipe = subprocess.Popen(["perl","C:\\Users\\Hariprabha\\Desktop\\NLPProject\\WNSemanticScore.pl", measure, word1, word2], stdout=subprocess.PIPE)
                wsim = float(pipe.stdout.read())
            else:
                wsim = 0.0
        else:
            pipe = subprocess.Popen(["perl","C:\\Users\\Hariprabha\\Desktop\\NLPProject\\WNSemanticScore.pl", measure, word1, word2], stdout=subprocess.PIPE)
            wsim = float(pipe.stdout.read())
    print(word1, word2, pos, wsim)
    return wsim

'''

# --------------------------------------------- TEXT SIMILARITY SCORE --------------------------------------------
def text_similarity(measure, answer1 = [], answer2 = [], idf_lst = []):
    num = 0.0
    denum = 0.0
    tsim = 0.0
    for i in range(len(answer1)):
        if i == 0:
            pos = "n"
        if i == 1:
            pos = "v"
        if i == 2:
            pos = "r"
        if i == 3:
            pos = "a"
        for word1 in answer1[i]:
            for lst in idf_lst:
                if word1 in lst:
                    idf1 = lst[1]
            maxsim = 0.0
            for word2 in answer2[i]:
                sim = 0.0
                sim = word_similarity(measure, word1, word2, pos)
                if sim > maxsim:
                    maxsim = sim
            num += maxsim*idf1
            denum += idf1
    if denum:
        tsim = num/denum
    else:
        tsim = num
    return tsim

for sa_key in student_answers:
    ma_key = sa_key
    ma_key = ma_key[0:ma_key.rfind('.')]
    semantic_scores[sa_key] = 0.5*(text_similarity("lin", model_answers[ma_key], student_answers[sa_key], idf[ma_key]) + text_similarity("path", student_answers[sa_key], model_answers[ma_key], idf[ma_key]))
print(semantic_scores)


# -------------------------------- SEMANTIC SCORE TO GRADES ----------------------------------------

def write_to_csv(semantic_scores = {}, scores = {}):
    f = open("C:\\Users\\Hariprabha\\Desktop\\NLPProject\\lin.csv", 'wb')
    try:
        writer = csv.writer(f)
        writer.writerow( ('Key', 'Similarity', 'Score') )
        for key in semantic_scores:
            writer.writerow( (key, semantic_scores[key], scores[key][0]) )
    finally:
        f.close()

write_to_csv(semantic_scores, scores)

