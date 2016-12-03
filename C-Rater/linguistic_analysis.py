import os
import pickle
import re
import subprocess

from autocorrect import spell
from nltk.parse import stanford
from nltk.tokenize import word_tokenize

import hobbs

os.environ[
    'STANFORD_PARSER'] = 'stanford-parser-full-2015-12-09'
os.environ[
    'STANFORD_MODELS'] = 'stanford-parser-full-2015-12-09'

parser = stanford.StanfordParser(model_path="englishPCFG.ser.gz")


def tokensToSentence(tokens):
    sentence = ""
    for word in tokens:
        sentence += word + " "
    return sentence

'''
java -cp OpenNLP_Parse_Tree_Generation-1.0-SNAPSHOT-jar-with-dependencies.jar csci544.opennlp_parse_tree_generation.parseTreeGenerator  "sentence to be parsed"
'''

'''def generate_parseTree_openNLP(sentence):
    proc = subprocess.Popen(['java', '-cp', 'OpenNLP_Parse_Tree_Generation-1.0-SNAPSHOT-jar-with-dependencies.jar', 'csci544.opennlp_parse_tree_generation.parseTreeGenerator', sentence.strip()], stdout=subprocess.PIPE)
    parseTree = proc.stdout.read()
    return parseTree.decode('utf-8').strip()[5:-1]'''

def generate_parseTree(sentence):
    return list(parser.raw_parse(sentence))

_digits = re.compile('\d')
_alphabets = re.compile('[A-Za-z]')

def spellCorrection(sentence):
    tokens = []
    '''if sentence[len(sentence) - 2] == ".":
        sentence = sentence[:-2]'''
    if sentence[len(sentence) - 2] == "?":
        sentence = sentence[:-2]
    for word in word_tokenize(sentence):
        if _alphabets.search(word) and not _digits.search(word):
            tokens.append(spell(word))
        else:
            tokens.append(word)
    return tokens

questions = {}
questionsReader = open(r'Dataset\\questions',"r")
for line in questionsReader:
    id = line.split(" ")[0]
    question = line[(len(id)+1):].lower().split("<stop>")[0]
    questions[id] = question

model_answers = {}
with open('outputs/model_sentences.txt', 'rb') as handle:
  model_answers = pickle.loads(handle.read())

parsed_answers = model_answers

for id in model_answers.keys():
    parseTrees = []
    spellCorrected_tokens = []
    for sent in model_answers[id]:
        tokens = spellCorrection(sent)
        parse_tree = generate_parseTree(tokensToSentence(tokens))
        parseTrees.append(parse_tree)
        spellCorrected_tokens.append(tokens)
    for tree in parseTrees:
        print(len(tree))
        if len(tree) == 1:
            question = questions[id]
            tokens = spellCorrection(questions[id])
            parse_tree = generate_parseTree(tokensToSentence(tokens))
            parsed_answers[id].add(hobbs.resolve_pronoun([parse_tree[0][0], tree[0][0][0]]))
        else:
            parsed_answers[id].add(hobbs.resolve_pronoun([tree[0][0][0], tree[1][0][0]]))

'''for id in model_answers.keys():
    list_for_combination = []
    alternate_sentences = []
    for sent in model_answers[id]:
        tokens = spellCorrection(sent)
        list1 = []
        for token in tokens:
            drf_list = []
            set1 = ()
            synonyms = wn.synsets(token)
            drf_list.append(token)
            if len(synonyms) > 0:
                lemma = synonyms[0].lemmas()
                drf_set = set()
                for drf in lemma[0].derivationally_related_forms():
                    st = str(drf)[7:-2]
                    s = st.split('.')[0]
                    drf_set.add(s)
                for drf in drf_set:
                    drf_list.append(drf)
            set1 = tuple(drf_list)
            list1.append(set1)
        list_for_combination.append(list1)
    final_combination_list = []
    for comb_list in list_for_combination:
        final_combination_list += comb_list
    final_alternate_answers = list(itertools.product(*final_combination_list))
    for answer in final_alternate_answers:
        ans = ""
        for word in answer:
            ans += word + " "
        alternate_sentences.append(ans.strip())
    alt_sentences = set()
    alt_sentences.update(alternate_sentences)
    parsed_answers[id].add(alt_sentences)'''

with open('outputs/parsed_sentences.txt', 'wb') as f:
    pickle.dump(parsed_answers, f)