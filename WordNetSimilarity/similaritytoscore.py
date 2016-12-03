#!/usr/bin/env python
from __future__ import division
import numpy as np
import pandas as pd
from sklearn import datasets, linear_model
from math import ceil

similarity_score = {}
train_data = {}
test_data = {}
check_data = {}

def get_data(file_name):
	data = pd.read_csv(file_name)
	simscr = {}
	for key, similarity, score in zip(data['Key'], data['Similarity'], data['Score']):
		simscr[key] = [[float(similarity)], float(score)]
	return simscr

similarity_score = get_data('/home/hmallyah/Desktop/SimilarityToGrades/lch.csv')

for key in similarity_score:
	if key[0: key.find('.')] not in ["11", "12"]:
		train_data[key] = similarity_score[key]
	else:
		test_data[key] = similarity_score[key][0][0]
		check_data[key] = similarity_score[key][1]

def linear_model_main(X_parameters = [],Y_parameters = [],predicts = {}):
	predictions = {}
	regr = linear_model.LinearRegression()
	regr.fit(X_parameters, Y_parameters)
	for key in predicts:
		predictions[key] = regr.predict(predicts[key])[0]
	return predictions

x = []
y = []
z = {}
for key in train_data:
	x.append(train_data[key][0])
	y.append(train_data[key][1])
for key in test_data:
	z[key] = test_data[key]

predictions = {}
predictions = linear_model_main(x,y,z)

def accuracy(predictions = {}, check_data = {}):
	count = 0
	for key in predictions:
		score = ceil(predictions[key])
		if score == check_data[key] or score == (check_data[key] - 0.5) or score == (check_data[key] + 0.5):
			count += 1
	return((float(count)/len(predictions))*100)

print(str(accuracy(predictions, check_data)))


