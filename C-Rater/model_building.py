from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import nltk
import itertools
import pickle

fileReader = open(r'Dataset\\answers',"r")
stop_words = set(stopwords.words('english'))
alternate_answers = {}
required_lexicons = {}
for line in fileReader:
    id = line.split(" ")[0]
    model_answer = line[(len(id)+1):].lower()
    sentences = model_answer.split("<stop>")
    del sentences[-1]
    alternate_senteces = []
    list_for_combination = []
    first_answer = ""
    for sent in sentences:
        #remove ',' and '.'(full-stop at the end of the sentence)
        #if sent[len(sent)-2] == ".":
        #    sent = sent[:-2]
        #sent = sent.replace(",","")
        rlWords = []
        filtered_sentence = []
        stemp = ""
        for i, token in enumerate(sent.split(" ")):
            if len(token) > 4:
                if token[-4:] == "<rl>":
                    stemp += token[:-4] + " "
                    rlWords.append(token[:-4])
                else:
                    stemp += token + " "
            else:
                stemp += token + " "
        required_lexicons[id] = rlWords
        tokens = word_tokenize(stemp.strip())
        filtered_sentence = [w for w in tokens if not w in stop_words and w in rlWords]
        pos_tag_list = nltk.pos_tag(tokens)
        synonyms_list = []
        for index, word in enumerate(pos_tag_list):
            synset = set()
            synset.add(word[0])
            first_answer += word[0] + " "
            if word[0] in filtered_sentence:
                synlist = []
                if word[1].startswith('N') or word[1].startswith('V'):
                    synonyms = wn.synsets(word[0])
                    for syn in synonyms:
                        if (word[1].startswith('N') and syn.name().split(".")[1] == 'n') or (word[1].startswith('V') and syn.name().split(".")[1] == 'v'):
                            if (" " in word[0] and "_" in syn.name().split(".")[0]) or (" " not in word[0] and "_" not in syn.name().split(".")[0]):
                                synlist.append(syn.name().split(".")[0].replace('_', ' '))
                synset.update(synlist)
            synonyms_list.append(synset)
        list_for_combination.append(synonyms_list)
    alternate_senteces.append(first_answer.strip())
    final_combination_list = []
    for comb_list in list_for_combination:
        final_combination_list += comb_list
    final_alternate_answers = list(itertools.product(*final_combination_list))
    for answer in final_alternate_answers:
        ans = ""
        for word in answer:
            ans += word + " "
        alternate_senteces.append(ans.strip())
    alt_sentences = set()
    alt_sentences.update(alternate_senteces)
    if id in alternate_answers.keys():
        alternate_answers[id].update(alt_sentences)
    else:
        alternate_answers[id] = alt_sentences

with open('outputs/model_sentences_s1q1.txt', 'wb') as f:
     pickle.dump(alternate_answers, f)

'''for id in required_lexicons.keys():
    required_lexicons[id] = list(k for k,_ in itertools.groupby(required_lexicons[id]))'''
with open('outputs\\required_lexicons_s1q1.txt', 'wb') as f:
    pickle.dump(required_lexicons, f)