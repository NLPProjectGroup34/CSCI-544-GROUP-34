from scipy import spatial
from TextPreprocessor import TextPreprocessor
from gensim.models import Word2Vec


class WikiTester:

    def __init__(self):
        self.training_set = None
        self.model = None
        self.avg_model_answer_vector = {}
        self.avg_student_answers_vector = {}

    def load_model(self):
        self.model = Word2Vec.load_word2vec_format('/Users/manali/Desktop/Himani_NLP/skip-enwik-full-sent-300-win10.bin', binary=True)

    def avg_string_vectors(self, word_list):
        wordcount = 0
        total = 0
        for word in word_list:
            if word in self.model:
                wordcount += 1
                total += self.model[word]
            else:
                print(word)
        if wordcount > 0:
            return total / wordcount
        else:
            return 0

    def convert_to_vectors(self, student_answers, model_answer):

        # Calculate model answer
        for key in model_answer.keys():
            self.avg_model_answer_vector[key] = self.avg_string(model_answer.get(key))
            self.avg_student_answers_vector[key] = []

        # Calculate student vector
        for answer in range(len(student_answers)):
            ans_no = student_answers[answer].pop(0)
            self.avg_student_answers_vector[ans_no].append(self.avg_string(student_answers[answer]))

    def calculate_similarity(self, vector1, vector2):
        sen1_sen2_similarity = 1 - spatial.distance.cosine(vector1, vector2)
        return sen1_sen2_similarity

    def readfile(self):
        t = TextPreprocessor()

        # Gets the list of model answer and student ans
        # Format of model answer:   {'1.1': ['word1', 'word2'], '1.2': ['word1', 'word2']]
        # Format of student answer: [['1.1', 'word1', 'word2'], ['1.1', 'word1', 'word2'],
        #                            ['1.2', 'word1', 'word2'], ['1.2', 'word1', 'word2']]
        model_answer = t.parse_file("/Users/manali/Desktop/Himani_NLP/ShortAnswerGrading_v2.0/data/sent/answers", False)
        student_answers = t.parse_file("/Users/manali/Desktop/Himani_NLP/ShortAnswerGrading_v2.0/data/sent/all", True)
        self.load_model()
        self.convert_to_vectors(student_answers, model_answer)
        for key in self.avg_model_answer_vector.keys():
            model_vector = self.avg_model_answer_vector(key)
            with open('/Users/manali/Desktop/Himani_NLP/OutputFolderWiki' + key + '.txt', 'w') as write_file:
                for answer in self.avg_student_answers_vector[key]:
                    write_file.write(self.calculate_similarity(model_vector, answer) + '\n')

# Main program
WikiTester().readfile()