import nltk
import pickle
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.parse.stanford import StanfordDependencyParser

path_to_jar = 'stanford-parser-full-2015-12-09\\stanford-parser.jar'
path_to_models_jar = 'stanford-parser-full-2015-12-09\\stanford-parser-3.6.0-models.jar'
dependency_parser = StanfordDependencyParser(path_to_jar=path_to_jar, path_to_models_jar=path_to_models_jar)

def writeToFile(fileName, content):
    fileWriter = open(fileName, 'w')
    fileWriter.write(content)
    fileWriter.close()
    return

def extract(sentence):
    f = {}
    result = dependency_parser.raw_parse(sentence)
    dep = result.__next__()
    triples = list(dep.triples())
    for triplet in triples:
        fList = []
        if ":" in triplet[1]:
            featureName = triplet[1].split(":")[0]
            fList.append(triplet[1].split(":")[1])
        else:
            featureName = triplet[1]
            fList.append("")
        fList.append(triplet[0][0])
        fList.append(triplet[0][1])
        fList.append(triplet[2][0])
        fList.append(triplet[2][1])
        if featureName not in f.keys():
            f[featureName] = []
        f[featureName].append(fList)
    return f

def getRequiredLexicons(sentence):
    rl = []
    sent = ""
    for token in sentence.split(" "):
        if len(token) > 4:
            if token[-4:].lower() == "<rl>":
                sent += token[:-4] + " "
                rl.append(token[:-4])
            else:
                sent += token + " "
        else:
            sent += token + " "
    return [rl, sent.strip()]

def getNMW(rl1, rl2):
    nmw = 0
    synlist2 = []
    for rl in rl2:
        for syn in wn.synsets(rl):
            if (" " in rl and "_" in syn.name().split(".")[0]) or (
                            " " not in rl and "_" not in syn.name().split(".")[0]):
                synlist2.append(syn.name().split(".")[0].replace('_', ' '))
    for rl in rl1:
        synlist1 = []
        for syn in wn.synsets(rl):
            if (" " in rl and "_" in syn.name().split(".")[0]) or (
                            " " not in rl and "_" not in syn.name().split(".")[0]):
                synlist1.append(syn.name().split(".")[0].replace('_', ' '))
        if not rl in rl2:
            if not rl in synlist2:
                if not any(i in synlist1 for i in rl2):
                    if not any(i in synlist1 for i in synlist2):
                        nmw += 1
    return nmw

def checkArgsMismatch(type1, type2, dep1, dep2):
    s1 = [s[3] for s in dep1[type1]]
    temp = s1
    for s in temp:
        for syn in wn.synsets(s):
            if (" " in s and "_" in syn.name().split(".")[0]) or (
                            " " not in s and "_" not in syn.name().split(".")[0]):
                s1.append(syn.name().split(".")[0].replace('_', ' '))
    s2 = [s[3] for s in dep2[type2]]
    temp = s2
    for s in temp:
        for syn in wn.synsets(s):
            if (" " in s and "_" in syn.name().split(".")[0]) or (
                            " " not in s and "_" not in syn.name().split(".")[0]):
                s2.append(syn.name().split(".")[0].replace('_', ' '))
    for idx1, i in enumerate(s1):
        for idx2, j in enumerate(s2):
            if i == j:
                if not WordNetLemmatizer().lemmatize(dep1[type1][idx1][1], 'v') == WordNetLemmatizer().lemmatize(dep2[type2][idx2][1], 'v'):
                    return True
                o1 = []
                o1.append(dep1[type1][idx1][1])
                for syn in wn.synsets(dep1[type1][idx1][1]):
                    if (" " in dep1[type1][idx1][1] and "_" in syn.name().split(".")[0]) or (
                                    " " not in dep1[type1][idx1][1] and "_" not in syn.name().split(".")[0]):
                        o1.append(syn.name().split(".")[0].replace('_', ' '))
                o2 = []
                o2.append(dep2[type2][idx2][1])
                for syn in wn.synsets(dep2[type2][idx2][1]):
                    if (" " in dep2[type2][idx2][1] and "_" in syn.name().split(".")[0]) or (
                                    " " not in dep2[type2][idx2][1] and "_" not in syn.name().split(".")[0]):
                        o2.append(syn.name().split(".")[0].replace('_', ' '))
                if not any(i in o1 for i in o2):
                    return  True
                else:
                    return False
    return True

def checkPassiveArgsMismatch(type1, type2, dep1, dep2):
    s1 = [s[3] for s in dep1[type1]]
    temp = s1
    for s in temp:
        for syn in wn.synsets(s):
            if (" " in s1 and "_" in syn.name().split(".")[0]) or (
                            " " not in s1 and "_" not in syn.name().split(".")[0]):
                s1.append(syn.name().split(".")[0].replace('_', ' '))
    s2 = [s[3] for s in dep2[type2]]
    temp = s2
    for s in temp:
        for syn in wn.synsets(s2):
            if (" " in s and "_" in syn.name().split(".")[0]) or (
                            " " not in s and "_" not in syn.name().split(".")[0]):
                s2.append(syn.name().split(".")[0].replace('_', ' '))
    for idx1, i in enumerate(s1):
        for idx2, j in enumerate(s2):
            if i == j:
                if not WordNetLemmatizer().lemmatize(dep1[type1][idx1][1], 'v') == WordNetLemmatizer().lemmatize(dep2[type2][idx2][1], 'v'):
                    return True
                o1 = []
                o1.append(dep1[type1][idx1][1])
                for syn in wn.synsets(dep1[type1][idx1][1]):
                    if (" " in dep1[type1][idx1][1] and "_" in syn.name().split(".")[0]) or (
                                    " " not in dep1[type1][idx1][1] and "_" not in syn.name().split(".")[0]):
                        o1.append(syn.name().split(".")[0].replace('_', ' '))
                o2 = []
                o2.append(dep2[type2][idx2][1])
                for syn in wn.synsets(dep2[type2][idx2][1]):
                    if (" " in dep2[type2][idx2][1] and "_" in syn.name().split(".")[0]) or (
                                    " " not in dep2[type2][idx2][1] and "_" not in syn.name().split(".")[0]):
                        o2.append(syn.name().split(".")[0].replace('_', ' '))
                if not any(i in o1 for i in o2):
                    return  True
                else:
                    return False
    return True

def get_Args_Roles_Mismatch(dep1, dep2):
    argsMismatch = []
    rolesMismatch = []
    if "nsubj" in dep1.keys():
        if "nsubj" in dep2.keys():
            if checkArgsMismatch("nsubj", "nsubj", dep1, dep2):
                argsMismatch.append("nsubj")
                rolesMismatch.append("nsubj_nsubj")
        elif "xsubj" in dep2.keys():
            if checkArgsMismatch("nsubj", "xsubj", dep1, dep2):
                argsMismatch.append("nsubj")
                rolesMismatch.append("nsubj_xsubj")
        elif "nsubjpass" in dep2.keys():
            if checkPassiveArgsMismatch("nsubj", "nsubjpass", dep1, dep2):
                argsMismatch.append("nsubj")
                argsMismatch.append("nsubj_nsubjpass")
    if "xsubj" in dep1.keys():
        if "nsubj" in dep2.keys():
            if checkArgsMismatch("xsubj", "nsubj", dep1, dep2):
                argsMismatch.append("xsubj")
                rolesMismatch.append("xsubj_nsubj")
        elif "xsubj" in dep2.keys():
            if checkArgsMismatch("xsubj", "xsubj", dep1, dep2):
                argsMismatch.append("xsubj")
                rolesMismatch.append("xsubj_xsubj")
        elif "nsubjpass" in dep2.keys():
            if checkPassiveArgsMismatch("xsubj", "nsubjpass", dep1, dep2):
                argsMismatch.append("xsubj")
                argsMismatch.append("xsubj_nsubjpass")
    if "nsubjpass" in dep1.keys():
        if "nsubj" in dep2.keys():
            if checkPassiveArgsMismatch("nsubj", "nsubjpass", dep2, dep1):
                argsMismatch.append("nsubjpass")
                argsMismatch.append("nsubjpass_nsubj")
        elif "xsubj" in dep2.keys():
            if checkPassiveArgsMismatch("xsubj", "nsubjpass", dep2, dep1):
                argsMismatch.append("nsubjpass")
                argsMismatch.append("nsubjpass_xsubj")
        elif "nsubjpass" in dep2.keys():
            if checkArgsMismatch("nsubjpass", "nsubjpass", dep1, dep2):
                argsMismatch.append("nsubjpass")
                rolesMismatch.append("nsubjpass_nsubjpass")
    if "dobj" in dep1.keys():
        if "dobj" in dep2.keys():
            if checkArgsMismatch("dobj", "dobj", dep1, dep2):
                argsMismatch.append("dobj")
                rolesMismatch.append("dobj_dobj")
        elif "iobj" in dep2.keys():
            if checkArgsMismatch("dobj", "iobj", dep1, dep2):
                argsMismatch.append("dobj")
                rolesMismatch.append("dobj_iobj")
        elif "pobj" in dep2.keys():
            if checkArgsMismatch("dobj", "pobj", dep1, dep2):
                argsMismatch.append("dobj")
                rolesMismatch.append("dobj_pobj")
    if "iobj" in dep1.keys():
        if "dobj" in dep2.keys():
            if checkArgsMismatch("iobj", "dobj", dep1, dep2):
                argsMismatch.append("iobj")
                rolesMismatch.append("iobj_dobj")
        elif "iobj" in dep2.keys():
            if checkArgsMismatch("iobj", "iobj", dep1, dep2):
                argsMismatch.append("iobj")
                rolesMismatch.append("iobj_iobj")
        elif "pobj" in dep2.keys():
            if checkArgsMismatch("pobj", "pobj", dep1, dep2):
                argsMismatch.append("iobj")
                rolesMismatch.append("pobj_pobj")
    if "pobj" in dep1.keys():
        if "dobj" in dep2.keys():
            if checkArgsMismatch("pobj", "dobj", dep1, dep2):
                argsMismatch.append("pobj")
                rolesMismatch.append("pobj_dobj")
        elif "iobj" in dep2.keys():
            if checkArgsMismatch("pobj", "iobj", dep1, dep2):
                argsMismatch.append("pobj")
                rolesMismatch.append("pobj_iobj")
        elif "pobj" in dep2.keys():
            if checkArgsMismatch("pobj", "pobj", dep1, dep2):
                argsMismatch.append("pobj")
                rolesMismatch.append("pobj_pobj")
    return [argsMismatch, rolesMismatch]

def findPolarityMismatch(neg1, neg2):
    negRoles = []
    negRole1 = []
    negRole2 = []
    for neg in neg1:
        negRole1.append(neg[1])
    for neg in neg2:
        negRole2.append(neg[1])
    for role in negRole1:
        if role not in negRole2:
            negRoles.append(role)
    for role in negRole2:
        if role not in negRole1:
            negRoles.append(role)
    return negRoles

def getPolarityMismatch(dep1, dep2):
    negRole = []
    if "neg" in dep1.keys() and "neg" not in dep2.keys():
        for neg in dep1["neg"]:
            negRole.append(neg[1])
    elif not "neg" in dep1.keys() and "neg" in dep2.keys():
        for neg in dep2["neg"]:
            negRole.append(neg[1])
    elif "neg" in dep1.keys() and "neg" in dep2.keys():
        negRole = findPolarityMismatch(dep1["neg"], dep2["neg"])
    return negRole

def generateFeatures(sentence1, sentence2, rl1, rl2):
    d = {}
    dep1 = extract(sentence1)
    dep2 = extract(sentence2)
    misMatch = get_Args_Roles_Mismatch(dep1, dep2)
    d['nmw'] = getNMW(rl1, rl2)
    d['argsMismatch'] = misMatch[0]
    d['argRoleIncompatible'] = misMatch[1]
    d['polarityMismatch'] = getPolarityMismatch(dep1, dep2)
    d['|RL|'] = len(rl1)
    d['|W|'] = len(sentence1.strip().split(" "))
    return d


def trainModel():
    train = []
    fileReader = open(r'Goldmap_Training_Data\\goldmap_training.txt',"r")
    for line in fileReader:
        data = line.split("|")
        label = data[0].strip()
        sentence1 = data[1].strip()
        sentence2 = data[2].strip()
        temp = getRequiredLexicons(sentence1)
        rl1 = temp[0]
        sentence1 = temp[1]
        temp = getRequiredLexicons(sentence2)
        rl2 = temp[0]
        sentence2 = temp[1]
        s= []
        s.append(generateFeatures(sentence1, sentence2, rl1, rl2))
        s.append(label)
        t = tuple(s)
        train.append(t)
    return train

required_lexicons_questions = {}
with open('required_lexicons.txt', 'rb') as handle:
  required_lexicons_questions = pickle.loads(handle.read())

model_answers = {}
with open('model_sentences.txt', 'rb') as handle:
  model_answers = pickle.loads(handle.read())

def generate_Test():
    test_all_students = {}
    for i in range(1, 31):
        required_lexicons_answers = {}
        fileName = "required_lexicons_student"+i+".txt"
        with open(fileName, 'rb') as handle:
            required_lexicons_answers = pickle.loads(handle.read())
        student_answers = {}
        fileName = "student"+i+"_answers.txt"
        with open(fileName, 'rb') as handle:
            student_answers = pickle.loads(handle.read())
        test = {}
        for questionNumber in student_answers.keys():
            for sentence1 in model_answers[questionNumber]:
                for sentence2 in student_answers[questionNumber]:
                    features = generateFeatures(sentence1, sentence2, required_lexicons_questions[questionNumber], required_lexicons_answers[questionNumber])
                    if questionNumber not in test:
                        test[questionNumber] = [features]
                    else:
                        test[questionNumber].append(features)
        test_all_students[i] = [test]
    return test_all_students

def getScores(features):
    score = 5
    if features['nmw'] == 0:
        return score
    score -= (2 * int(features['nmw'])) / float(features['|RL|'])
    if not len(features['argsMismatch']) == 0:
        y = 0.0
        for args in features['argRoleIncompatible']:
            arg1 = args.split("_")[0]
            arg2 = args.split("_")[1]
            if arg1 == "nsubj" and arg2 == "nsubj":
                y += 1.0
            if arg1 == "nsubj" and arg2 == "xsubj":
                y += 0.5
            if arg1 == "nsubj" and arg2 == "nsubjpass":
                y += 0.25
            if arg1 == "xsubj" and arg2 == "nsubj":
                y += 0.5
            if arg1 == "xsubj" and arg2 == "xsubj":
                y += 1.0
            if arg1 == "xsubj" and arg2 == "nsubjpass":
                y += 0.25
            if arg1 == "nsubjpass" and arg2 == "nsubj":
                y += 0.25
            if arg1 == "nsubjpass" and arg2 == "xsubj":
                y += 0.25
            if arg1 == "nsubjpass" and arg2 == "nsubjpass":
                y += 1.0
            if arg1 == "dobj" and arg2 == "dobj":
                y += 1.0
            if arg1 == "dobj" and arg2 == "iobj":
                y += 0.25
            if arg1 == "dobj" and arg2 == "pobj":
                y += 0.25
            if arg1 == "iobj" and arg2 == "dobj":
                y += 0.25
            if arg1 == "iobj" and arg2 == "iobj":
                y += 1.0
            if arg1 == "iobj" and arg2 == "pobj":
                y += 0.25
            if arg1 == "pobj" and arg2 == "dobj":
                y += 0.25
            if arg1 == "pobj" and arg2 == "iobj":
                y += 0.25
            if arg1 == "pobj" and arg2 == "pobj":
                y += 1.0
        y = y/len(features['argRoleIncompatible'])
        score -= y/18
    if not len(features['polarityMismatch']) == 0:
        score -= len(features['polarityMismatch']) / float(features['|W|'])
    return score

def classify(test_all_students):
    i = 1
    for test in test_all_students:
        final_scores = []
        for questionNumber in test.keys():
            scores = []
            for featureset in test[questionNumber]:
                pdist = classifier.prob_classify(featureset)
                if pdist.prob('1') >= 0.5:
                    scores.append(getScores(featureset))
            final_scores.append(max(scores))
        fileName = "student"+i+"_score.txt"
        content = ""
        for score in final_scores:
            content += score + "\n"
        writeToFile(fileName, content.strip())
    return

train = trainModel()
writeToFile('outputs/goldmap_trainingset.txt', train)

classifier = nltk.MaxentClassifier.train(train, 'GIS', trace=0, max_iter=1000)