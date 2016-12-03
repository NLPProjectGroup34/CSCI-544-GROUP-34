import gensim
import math
import numpy as np
from scipy import spatial
from TextPreprocessor import TextPreprocessor
from gensim.models import Word2Vec


class WikiTester:

    def __init__(self):
        self.training_set = None
        self.model = None
        self.avg_model_answer_vector = {}
        self.avg_student_answers_vector = {}

    def load_model(self, new_list):
        self.model = Word2Vec.load('D:/Studies/USC/3rdSem/CSCI544/GroupProjectData/StackOverFlowModel')

    def avg_string_vectors(self, word_list, dimensions):
        total = np.zeros(dimensions)
        for word in word_list:
            if word in self.model:
                total += self.model[word]
        if np.linalg.norm(total) > 0:
             return total / np.linalg.norm(total)
        else:
            return total

    def convert_to_vectors(self, student_answers, model_answer, dimensions):

        # Calculate model answer
        for key in model_answer.keys():
            self.avg_model_answer_vector[key] = self.avg_string_vectors(model_answer.get(key), dimensions)
            self.avg_student_answers_vector[key] = []

        # Calculate student vector
        for answer in range(len(student_answers)):
            ans_no = student_answers[answer].pop(0)

            self.avg_student_answers_vector[ans_no].append(self.avg_string_vectors(student_answers[answer], dimensions))

    def calculate_similarity(self, vector1, vector2):
        if np.count_nonzero(vector1) == 0 or np.count_nonzero(vector2) == 0:
            return 0.0
        sen1_sen2_similarity = 1 - spatial.distance.cosine(vector1, vector2)
        return sen1_sen2_similarity

    def readfile(self):
        t = TextPreprocessor()

        # Gets the list of model answer and student ans
        # Format of model answer:   {'1.1': ['word1', 'word2'], '1.2': ['word1', 'word2']]
        # Format of student answer: [['1.1', 'word1', 'word2'], ['1.1', 'word1', 'word2'],
        #                            ['1.2', 'word1', 'word2'], ['1.2', 'word1', 'word2']]
        model_answer = t.parse_file("D:/Studies/USC/3rdSem/CSCI544/GroupProjectData/ShortAnswerGrading_v2.0/data/sent/answers", False)
        student_answers = t.parse_file("D:/Studies/USC/3rdSem/CSCI544/GroupProjectData/ShortAnswerGrading_v2.0/data/sent/all", True)
        model_answer_list = []
        for keys in model_answer.keys():
            model_answer_list.append(model_answer[keys])
        print(model_answer_list)
        self.load_model(model_answer_list)
        dimensions = len(self.model[next(iter(self.model.vocab.keys()))])
        self.convert_to_vectors(student_answers, model_answer, dimensions)

        for key in self.avg_model_answer_vector.keys():
            print(key)
            model_vector = self.avg_model_answer_vector[key]
            writer = open('D:/Studies/USC/3rdSem/CSCI544/GroupProjectData/OutputFolderStackoverflow/' + key + '.txt', 'w')
            for answer in self.avg_student_answers_vector[key]:
                similarity_score = np.float64(self.calculate_similarity(model_vector, answer)).item()
                score = 0
                if similarity_score >= 0.97:
                    score = 5
                elif similarity_score >= 0.89:
                    score = 4.5
                elif similarity_score >= 0.86:
                    score = 4
                elif similarity_score >= 0.85:
                    score = 3
                elif similarity_score >= 0.80:
                    score = 2
                elif similarity_score >= 0.75:
                    score = 1
                elif similarity_score > 0:
                    score = 0.5
                else:
                    score = 0
                writer.write(str(score) + '\n')
            writer.close()

# Main program
WikiTester().readfile()