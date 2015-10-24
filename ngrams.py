'''
Joshua Meyer

Given a corpus (text file), output a model of n-grams in ARPA format
USAGE: $ python3 ngrams.py
'''
from tokenize_corpus import tokenize_file
import operator
from collections import Counter
import numpy as np
import re




def get_user_input():
    fileName = input("Enter filepath here: ")
    smoothing = input("Pick your flavor of smoothing...\n"+
                      "Enter 'laplace' or 'lidstone' or 'none' here: ")
    if smoothing == 'lidstone':
        _lambda = float(input("Choose your value for Lidstone's Lambda\n"+
                      "Enter a decimal here: "))
    else:
        _lambda = None
    return fileName, smoothing, _lambda


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


def get_unigram_model(uniProbDict):
    ''' 
    p(A) = log(count(A)/length(CORPUS))
    '''
    unigramProbs={}
    for key,value in uniProbDict.items():
        unigramProbs[key] = np.log(value)
    return unigramProbs


def get_bigram_model(uniProbDict,biProbDict):
    '''
    p(B|A) =  log(p(A_B)/p(A))
    '''
    loggedProbs={}
    for A_B, pA_B in biProbDict.items():
        pA = uniProbDict[A_B[0]]
        pBgivenA = pA_B/pA
        loggedProbs[A_B] = np.log(pBgivenA)
    return loggedProbs


def get_trigram_model(biProbDict,triProbDict):
    '''
    p(C|A_B) =  log(p(A_B_C)/p(A_B))
    '''
    loggedProbs={}
    for A_B_C, pA_B_C in triProbDict.items():
        pA_B = biProbDict[A_B_C[0:2]]
        pCgivenA_B = pA_B_C/pA_B
        loggedProbs[A_B_C] = np.log(pCgivenA_B)
    return loggedProbs


def print_to_file(unigramModel,bigramModel,trigramModel):
    outFile = open('kyrgyz.lm', mode='wt', encoding='utf-8')
    nUnigrams = len(unigramModel)
    nBigrams = len(bigramModel)
    nTrigrams = len(trigramModel)
    
    print('\data\\', end='\n', file=outFile)
    print(('ngram 1=' + str(nUnigrams)), end='\n', file=outFile)
    print(('ngram 2=' + str(nBigrams)), end='\n', file=outFile)
    print(('ngram 3=' + str(nTrigrams)), end='\n', file=outFile)
    
    print('\n1-grams:', end='\n', file=outFile)
    sortedDict = sorted(unigramModel.items(), key=operator.itemgetter(1),
                        reverse=True)
    for unigram,logProb in sortedDict:
        print((str(logProb) +' '+ unigram),
              end='\n', file=outFile)

    print('\n2-grams:', end='\n', file=outFile)
    sortedDict = sorted(bigramModel.items(), key=operator.itemgetter(1),
                        reverse=True)
    for bigram,logProb in sortedDict:
        print((str(logProb) +' '+ bigram[0] +' '+ bigram[1]),
              end='\n',file=outFile)

    print('\n3-grams:', end='\n', file=outFile)
    sortedDict = sorted(trigramModel.items(), key=operator.itemgetter(1),
                        reverse=True)
    for trigram,logProb in sortedDict:
        print((str(logProb) +' '+ trigram[0] +' '+ trigram[1] +' '+ trigram[2]),
              end='\n', file=outFile)

        
if __name__ == "__main__":
    fileName,smoothing,_lambda = get_user_input()

    unigrams = tokenize_file(fileName)
    bigrams = get_ngrams(unigrams, 2)
    trigrams = get_ngrams(unigrams, 3)
    
    uniProbDict, uniProbUnSeen = apply_smoothing(unigrams,1,smoothing,_lambda)
    biProbDict, biProbUnSeen = apply_smoothing(bigrams,2,smoothing,_lambda)
    triProbDict, triProbUnSeen = apply_smoothing(trigrams,3,smoothing,_lambda)

    unigramModel = get_unigram_model(uniProbDict)
    bigramModel = get_bigram_model(uniProbDict,biProbDict)
    trigramModel = get_trigram_model(biProbDict,triProbDict)

    print_to_file(unigramModel,bigramModel,trigramModel)
