import os
import math

'''
Read the Student Score generated
'''
student_scores = []
for i in range(1,30):
    fileName = "student" + i + "_score.txt"
    fileReader = open(fileName, "r", encoding="latin1")
    scores = []
    for line in fileReader:
        scores.append(line.strip())
    fileReader.close()
    student_scores.append(scores)

'''
Read the scores given by human greaders
'''
model_scores = []
for i in range (1,31):
    model_scores.append([])
modelScoresDir = "Dataset\\Scores"
for dirName, subdirList, fileList in os.walk(modelScoresDir):
        for file in fileList:
            if file == "ave":
                fileReader = open(os.path.join(modelScoresDir,fileName), "r", encoding="latin1")
                i = 0
                for line in fileReader:
                    model_scores[i].append(line.strip())
                    i += 1

'''
Calculated the Accuracy
'''

accuracies = []
for i in range(0, len(student_scores)):
    studentScores = student_scores[i]
    modelScores = model_scores[i]
    accuracy = 0.0
    correctScore = 0
    totalScore = len(studentScores)
    for j in range(0, len(studentScores)):
        if math.abs(studentScores[j]-modelScores[j]) <= 0.5:
            correctScore += 1
    accuracy = correctScore / totalScore * 100
    accuracies.append(accuracy)

sum = 0.0
for accuracy in accuracies:
    sum += accuracy
average_accuracy = sum / len(accuracies)

'''
Print the Evaluation Result
'''
print(average_accuracy)