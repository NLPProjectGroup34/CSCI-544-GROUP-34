from gensim.parsing import PorterStemmer
from nltk.corpus import stopwords


class TextPreprocessor:
    def __init__(self):
        self.stop = set(stopwords.words('english'))
        self.global_stemmer = PorterStemmer()

    # Stem the word. It returns base form of a word
    def stem(self, word):
        stemmed = self.global_stemmer.stem(word)
        return stemmed

    # Removes stop words from a sentence
    def remove_stopwords(self, sentence):
        tokens = []

        # Currently this only removes fullstop at the end
        for i in sentence.lower().split():
            if i not in '<stop>':
                if i.endswith('.'):
                    i = i.replace(".", "")
                elif i.endswith(','):
                    i = i.replace(",", "")
                tokens.append(i)

        # if i not in self.stop and i not in '<stop>':
               # i = i.replace(",", "")
               # i = i.replace(".", "")
              #  i = self.stem(i)
              #  tokens.append(i)

        return tokens

    # Parse the file and generates training set
    def parse_file(self, filename, is_student_answer):
        with open(filename) as f:
            content = f.readlines()
        if is_student_answer:
            file_list = []
            for line in content:
                line_list = self.remove_stopwords(line)
                file_list.append(line_list)
            return file_list
        else:
            file_dict = {}
            for line in content:
                line_list = self.remove_stopwords(line)
                file_dict[line_list.pop(0)] = line_list
            return file_dict


# t = TextPreprocessor()
# model_answer = t.parse_file("D:/Studies/USC/3rdSem/CSCI544/GroupProjectData/ShortAnswerGrading_v2.0/data/sent/answers", False)
# student_answers = t.parse_file("D:/Studies/USC/3rdSem/CSCI544/GroupProjectData/ShortAnswerGrading_v2.0/data/sent/all", True)
# print(model_answer)
# print(student_answers)


