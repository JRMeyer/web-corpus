'''
Joshua Meyer

This script puts out joint probabilities for sentences from a test corpus given
some training corpus. 

INPUT: path to training corpus and test corpus
OUTPUT: joint probabilities from test corpus, conditioned on training corpus

USAGE: $ python3 ngrams.py
'''
from tokenize_corpus import tokenize_file
import sys
from collections import Counter
import numpy as np
import re


def get_ngrams(tokens, n):
    ngrams=[]
    # take unigrams and concatenate them into ngrams
    for i in range(len(tokens)-(n-1)):
        ngrams.append(tuple(tokens[i:i+n]))
    return ngrams
            

def apply_smoothing(ngrams, ngramOrder, smoothing, _lambda):
    '''
    make a dictionary of probabilities, where the key is the ngram and the
    value is the frequency of that word over the number of tokens in corpus
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


def get_user_input():
    fileName = input("Enter filepath here: ")
    ngramOrder = int(input("Do you want unigrams or bigrams?\n"+
                      "Enter a 1 or 2 here: "))
    smoothing = input("Pick your flavor of smoothing...\n"+
                      "Enter 'laplace' or 'lidstone' or 'none' here: ")
    if smoothing == 'lidstone':
        _lambda = float(input("Choose your value for Lidstone's Lambda\n"+
                      "Enter a decimal here: "))
    else:
        _lambda = None
    return fileName, ngramOrder, smoothing, _lambda


def get_unigram_probs(uniProbDict):
    ''' 
    take the logs of the probs
    '''
    unigramProbs={}
    for key,value in uniProbDict.items():
        unigramProbs[key] = np.log(value)
    return unigramProbs


def get_bigram_probs(uniProbDict,biProbDict):
    '''
    p(B|A) =  log(p(A,B)/p(A))
    '''
    loggedProbs={}
    for A_B, pA_B in biProbDict.items():
        pA = uniProbDict[A_B[0]]
        pBgivenA = pA_B/pA
        loggedProbs[A_B] = np.log(pBgivenA)
    return loggedProbs


def print_to_file(unigramProbs,bigramProbs):
    nUnigrams = len(unigramProbs)
    nBigrams = len(bigramProbs)
    outFile = open('kyrgyz.lm', mode='wt', encoding='utf-8')
    
    print('\data\\', end='\n', file=outFile)
    print(('ngram 1=' + str(nUnigrams)), end='\n', file=outFile)
    print(('ngram 2=' + str(nBigrams)), end='\n', file=outFile)
    
    print('\n1-grams:', end='\n', file=outFile)
    for unigram,logProb in unigramProbs.items():
        print((unigram +' '+ str(logProb)), end='\n', file=outFile)

    print('\n2-grams:', end='\n', file=outFile)
    for bigram,logProb in bigramProbs.items():
        print((bigram[0] +' '+ bigram[1] +' '+ str(logProb)), end='\n', file=outFile)

        
if __name__ == "__main__":
    fileName,ngramOrder,smoothing,_lambda = get_user_input()

    unigrams = tokenize_file(fileName)
    bigrams = get_ngrams(unigrams, 2)
    
    uniProbDict, uniProbUnSeen = apply_smoothing(unigrams,1,smoothing,_lambda)
    biProbDict, biProbUnSeen = apply_smoothing(bigrams,2,smoothing,_lambda)

    unigramProbs = get_unigram_probs(uniProbDict)
    bigramProbs = get_bigram_probs(uniProbDict,biProbDict)

    print_to_file(unigramProbs,bigramProbs)
