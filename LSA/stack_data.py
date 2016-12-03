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
import xml.etree.cElementTree as etree
from xml.dom import minidom
import glob
import codecs
import pickle

stopwords_list = []
stopwords_file = open(r'/Users/shwetha/Desktop/stopwords.txt').readlines()
for lines in stopwords_file:
    lines = lines.replace("\n","")
    stopwords_list.append(lines)


list_of_post_files = []
list_of_post_history_files = []
list_of_comments_files = []


content_of_post_files = []
updated_content_of_post_files = []

content_of_post_history_files = []
updated_content_of_post_history_files = []

content_of_comments_files = []
updated_content_of_comments_files = []

all_contents_list = []

for root, dirs, files in os.walk(r'/Users/shwetha/Desktop/engineering.stackexchange.com/'):
    for dir in dirs:
        if (dir == "posts"):
            path = os.path.join(root, dir)
            for file in glob.glob(os.path.join(path, '*.xml')):
                list_of_post_files.append(file)

        if (dir == "posts_history"):
            path = os.path.join(root, dir)
            for file in glob.glob(os.path.join(path, '*.xml')):
                list_of_post_history_files.append(file)

        if (dir == "comments"):
            path = os.path.join(root, dir)
            for file in glob.glob(os.path.join(path, '*.xml')):
                list_of_comments_files.append(file)

for file in list_of_post_files:
    xmldoc = minidom.parse(file)
    itemlist = xmldoc.getElementsByTagName('row')
    for s in itemlist:
        content = s.attributes['Body'].value
        content_of_post_files.append(content)

for line in content_of_post_files:
    line = line.replace("<li>","").replace("<p>","").replace("</p>","").replace("</li>","").replace("<ol>","").replace("</ol","").replace("<ul>","").replace("</ul>","").replace("</a>","").replace("<a href","")
    for word in stopwords_list:
        if word in line:
            line = line.replace(word,"")
            updated_content_of_post_files.append(line)

for file in list_of_post_history_files:
    xmldoc = minidom.parse(file)
    itemlist = xmldoc.getElementsByTagName('row')
    for s in itemlist:
        content = s.attributes['Text'].value
        content_of_post_history_files.append(content)

for line in content_of_post_history_files:
    line = line.replace("<li>","").replace("<p>","").replace("</p>","").replace("</li>","").replace("<ol>","").replace("</ol","").replace("<ul>","").replace("</ul>","").replace("</a>","").replace("<a href","")
    for word in stopwords_list:
        if word in line:
            line = line.replace(word,"")
            updated_content_of_post_files.append(line)

for file in list_of_comments_files:
    xmldoc = minidom.parse(file)
    itemlist = xmldoc.getElementsByTagName('row')
    for s in itemlist:
        content = s.attributes['Text'].value
        content_of_comments_files.append(content)

for line in content_of_comments_files:
    line = line.replace("<li>","").replace("<p>","").replace("</p>","").replace("</li>","").replace("<ol>","").replace("</ol","").replace("<ul>","").replace("</ul>","").replace("</a>","").replace("<a href","")
    for word in stopwords_list:
        if word in line:
            line = line.replace(word,"")
            updated_content_of_comments_files.append(line)

file_contents = updated_content_of_comments_files + updated_content_of_post_files
all_contents_list = file_contents + updated_content_of_post_history_files

with open(r'/Users/shwetha/Desktop/engineering.stackexchange.com/stack_data.txt', 'wb') as f:
    pickle.dump(updated_content_of_post_files, f)