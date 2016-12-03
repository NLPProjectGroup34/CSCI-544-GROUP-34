import os
import sys

avg_score_model = {}
student_score_model = {}


def traverse_directory_train(path, avg_score, booleanvar):
    for dirName, subDirList, fileList in os.walk(path[0]):
        for file in fileList:
            if (booleanvar and file in 'ave'):
                w = open(os.path.join(dirName, file), "r", encoding="latin1")
                avg_score[os.path.basename(os.path.normpath(dirName))] = w.read().split()
            elif not booleanvar:
                w = open(os.path.join(dirName, file), "r", encoding="latin1")
                avg_score[os.path.splitext(file)[0]] = w.read().split()


def classify_files(avg_score_model, student_score_model):
    result = {}
    for key in student_score_model.keys():
        result[key] = []
        avg_list = avg_score_model.get(key)
        stud_list = student_score_model.get(key)
        for ans_no in range(len(avg_list)):
            avg_no_float = float(avg_list[ans_no])
            stud_no_float = float(stud_list[ans_no])
            if (avg_no_float == stud_no_float) or (avg_no_float + 0.5 == stud_no_float) or (avg_no_float - 0.5 == stud_no_float):
                result[key].append(True)
            else:
                result[key].append(False)
    return result

def cal_precision(result):
    precision = {}
    for key in result.keys():
        true_counter = result[key].count(True)
        total_ans = len(result[key])
        precision[key] = true_counter / total_ans
    return precision

def cal_avg_precision(precision):
    sum = 0
    for key in precision.keys():
        sum += precision[key]
    return sum / len(precision)

# Change the folder name according to the method
traverse_directory_train(['D:/Studies/USC/3rdSem/CSCI544/GroupProjectData/ShortAnswerGrading_v2.0/data/scores/'], avg_score_model, True)
traverse_directory_train(['D:/Studies/USC/3rdSem/CSCI544/GroupProjectData/OutputFolderBrownSkipGram/'], student_score_model, False)
result = classify_files(avg_score_model,student_score_model)
precision = cal_precision(result)
print("Precision" + str(cal_avg_precision(precision)))
