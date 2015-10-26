'''
Joshua Meyer

Given a corpus (text file), output a model of n-grams in ARPA format
USAGE: $ python3 q1.py
'''
from tokenize_corpus import *
import operator
from collections import Counter
import numpy as np
import re




def get_user_input():
    fileName = input("Enter filepath here: ")
    fTest = input("Enter test filepath here: ")
    smoothing = input("Pick your flavor of smoothing...\n"+
                      "Enter 'laplace' or 'lidstone' or 'none' here: ")
    if smoothing == 'lidstone':
        _lambda = float(input("Choose your value for Lidstone's Lambda\n"+
                      "Enter a decimal here: "))
    else:
        _lambda = None
    return fileName, fTest, smoothing, _lambda


def get_ngrams(tokens, n):
    ngrams=[]
    # special case for unigrams
    if n==1:
        for token in tokens:
            # we need parentheses and a comma to make a tuple
            ngrams.append((token,))
    # general n-gram case
    else:
        for i in range(len(tokens)-(n-1)):
            ngrams.append(tuple(tokens[i:i+n]))
    return ngrams


def get_prob_dict(ngrams, ngramOrder, smoothing, _lambda):
    '''
    Make a dictionary of probabilities, where the key is the ngram.

    Without smoothing, we have: p(X) = freq(X)/NUMBER_OF_NGRAMS
    '''
    if smoothing == 'none':
        numSmooth = 0
        denominator =  len(ngrams)
        probUnSeen = 1/denominator
        
    elif smoothing == "laplace":
        numSmooth = 1
        denominator =  (len(ngrams)+ len(ngrams)**ngramOrder)
        probUnSeen = 1/denominator
        
    elif smoothing == 'lidstone':
        numSmooth = _lambda
        denominator = (len(ngrams) + (len(ngrams)**ngramOrder)*_lambda)
        probUnSeen = _lambda/denominator

    probDict={}
    for key, value in Counter(ngrams).items():
        probDict[key] = ((value + numSmooth) / denominator)

    return probDict, probUnSeen


def get_ngram_model(probDict):
    '''
    Given a dictionary of nGrams for some corpus, compute the conditional
    probabilities for higher order nGrams. There must be all nGrams already in
    the dict leading up to the highest order. IE, if the dict has trigrams, it
    *must* also have bigrams and unigrams. 

    p(N|N_MINUS_ONE) = log(p(N)/p(N_MINUS_ONE))

    p(A) = log(p(A))
    p(B|A) =  log(p(A_B)/p(A))
    p(C|A_B) =  log(p(A_B_C)/p(A_B))
    '''
    loggedProbs={}
    for nGram, nGramProb in probDict.items():
        if len(nGram) == 1:
            loggedProbs[nGram] = np.log(nGramProb)
        else:
            nMinus1Gram = nGram[:(len(nGram)-1)]
            nMinus1GramProb = probDict[nMinus1Gram]
            condNgramProb = nGramProb/nMinus1GramProb
            loggedProbs[nGram] = np.log(condNgramProb)
    return loggedProbs



def print_joint_prob(fileName, probDict, probUnSeen):
    '''
    make predictions on test corpus, given probabilities from training corpus
    '''
    f = open(fileName)
    for line in f:
        probs=[]
        tokens = tokenize_line(line,2,tags=False)
        for bigram in get_ngrams(tokens,2):
            try:
                probs.append(probDict[bigram])
            except:
                probs.append(np.log(probUnSeen))
        print(np.prod(probs))

        
if __name__ == "__main__":
    fileName,fTest,smoothing,_lambda = get_user_input()

    unigrams=[]
    bigrams=[]
    f = open(fileName)
    numSentences=0
    for line in f:
        tokens = tokenize_line(line,1,tags=True)
        for unigram in get_ngrams(tokens,1):
            unigrams.append(unigram)

        tokens = tokenize_line(line,2,tags=True)
        for bigram in get_ngrams(tokens,2):
            bigrams.append(bigram)
        numSentences+=1

    # we need these to calulate our conditional probabilities later on
    unigrams = unigrams + [('#',)]*numSentences 
        
    uniProbDict, uniProbUnSeen = get_prob_dict(unigrams,1,smoothing,_lambda)
    biProbDict, biProbUnSeen = get_prob_dict(bigrams,2,smoothing,_lambda)

    nGramProbDict = {}
    for d in [uniProbDict,biProbDict]:
        for key,value in d.items():
            nGramProbDict[key] = value

    condProbDict = get_ngram_model(nGramProbDict)

    print_joint_prob(fTest,condProbDict,biProbUnSeen)
    
