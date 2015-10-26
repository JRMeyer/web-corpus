import re

def tokenize_line(line,n,tags):
    '''
    (1) lower all text 
    (2) strip newlines
    (3) split line on whitespace
    (6) optionally pad the line
    (7) return tokens
    '''
    tokens=[]
    line = line.lower().rstrip()
    for token in line.split(' '):
        if tags == True:
            tokens.append(token.split('_')[0])
        elif tags == False:
            tokens.append(token)
    tokens = pad_line(tokens,n)
    return tokens

    
def pad_line(tokens, n):
    # pad the line if we need to
    if n == 1:
        tokens = tokens
    else:
        tokens = ['#']*(n-1) + tokens
    return tokens




