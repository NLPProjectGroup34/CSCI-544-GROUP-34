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
import pickle


with open(r"/Users/shwetha/Desktop/engineering.stackexchange.com/stack_data.txt", 'rb') as f:
    stack_data = pickle.load(f)

training_data = stack_data


mydoclist = training_data
print(len(mydoclist))
print(type(mydoclist))


for doc in mydoclist:
    tf = Counter()
    for word in doc.split():
        tf[word] +=1
    #print (tf.items())
#print ('\n')

def build_lexicon(corpus):
    lexicon = set()
    for doc in corpus:
        lexicon.update([word for word in doc.split()])
    return lexicon

#Build the list of unique words in all documents and call it vocabulary
vocabulary = build_lexicon(mydoclist)
#print ('Our vocabulary vector (unique word list) is [' + ', '.join(list(vocabulary)) + ']')
#print ('\n')


#write length of my doclist to a file
write_mydoclist = open("/Users/shwetha/Desktop/NLP_PROJECT/LSA_trained_data/doclength.txt","w")
write_mydoclist.write(str(len(mydoclist)))
write_mydoclist.close()

#write the vocabulary to a file each word is written on new line but the code vocabulary was of type set
vocab_file = open("/Users/shwetha/Desktop/NLP_PROJECT/LSA_trained_data/vocabulary.txt","w")
for v in vocabulary:
    vocab_file.write(v)
    vocab_file.write("\n")
vocab_file.close()



#Return frequency of term in the document
def tf(term, document):
    return freq(term, document)

def freq(term, document):
    return document.split().count(term)

doc_term_matrix = []
for doc in mydoclist:
    #print 'The doc is "' + doc + '"'
    #For each word in vocabulary, find the count of occurrence in each document
    tf_vector = [tf(word, doc) for word in vocabulary]
    tf_vector_string = ', '.join(format(freq,'d') for freq in tf_vector)
    #print 'The tf vector for Document %d is [%s]' % ((mydoclist.index(doc) + 1), tf_vector_string)
    doc_term_matrix.append(tf_vector)

#print '\n'
#print 'All combined, here is our master document term matrix: '
#print doc_term_matrix

#Normalize the doc_term_matrix
def l2_normalizer(vec):
    denom = np.sum([el**2 for el in vec])
    return [(el / math.sqrt(denom)) for el in vec]

doc_term_matrix_l2 = []
for vec in doc_term_matrix:
    doc_term_matrix_l2.append(l2_normalizer(vec))

#print '\n'
#print 'A regular old document term matrix: '
#print np.matrix(doc_term_matrix)
#print '\n'
#print '\nA document term matrix with row-wise L2 norms of 1:'
#print np.matrix(doc_term_matrix_l2)
#print '\n'

#IDF frequency weighting
def numDocsContaining(word, doclist):
    doccount = 0
    for doc in doclist:
        if freq(word, doc) > 0:
            doccount +=1
    return doccount

def idf(word, doclist):
    n_samples = len(doclist)
    df = numDocsContaining(word, doclist)
    return np.log(n_samples / 1+df)

my_idf_vector = [idf(word, mydoclist) for word in vocabulary]

#print 'Our vocabulary vector is [' + ', '.join(list(vocabulary)) + ']'
#print 'The inverse document frequency vector is [' + ', '.join(format(freq, 'f') for freq in my_idf_vector) + ']'


def build_idf_matrix(idf_vector):
    idf_mat = np.zeros((len(idf_vector), len(idf_vector)))
    np.fill_diagonal(idf_mat, idf_vector)
    return idf_mat

my_idf_matrix = build_idf_matrix(my_idf_vector)
#print '\n'
#print 'My IDF matrix is\n'
#print my_idf_matrix

#Build TF-IDF
doc_term_matrix_tfidf = []

# performing tf-idf matrix multiplication
for tf_vector in doc_term_matrix:
    doc_term_matrix_tfidf.append(np.dot(tf_vector, my_idf_matrix))

# normalizing
doc_term_matrix_tfidf_l2 = []
for tf_vector in doc_term_matrix_tfidf:
    doc_term_matrix_tfidf_l2.append(l2_normalizer(tf_vector))

#print '\nMy TFIDF matrix is \n'
#print vocabulary

#print(np.matrix(doc_term_matrix_tfidf_l2))  # np.matrix() just to make it easier to look at

final_matrix  = np.matrix(doc_term_matrix_tfidf_l2)

#write the tf-idf to a text file
np.savetxt("/Users/shwetha/Desktop/NLP_PROJECT/LSA_trained_data/matrix.txt", final_matrix)


global U, s, V
U, s, V = svd(zip(*doc_term_matrix_tfidf_transpose))


#print '\nPrinting U\n'
#print(U)
#print '\nPrinting s\n'
#print(s)
#print '\nPrinting V\n'
#print(V)

def create_word_doc(vocabulary, doc_term_matrix):
    word_doc={}
    count = 0
    for word in vocabulary:
        word_occurance=0
        for item in doc_term_matrix:
            word_occurance+=item[count]
        word_doc[vocabulary[count]] = word_occurance
        count += 1
    return word_doc

word_doc = create_word_doc(list(vocabulary), doc_term_matrix)

json.dump(word_doc, open("/Users/shwetha/Desktop/NLP_PROJECT/LSA_trained_data/word_doc.txt", 'w'))
