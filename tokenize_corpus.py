import re

def tokenize_file(fileName):
    '''
    Given a file: (1) lower all text, (2) strip newlines,
    (3) tokenize on whitespace, (4) throw out numbers,
    (5) remove non-alphabetic characters, (6) return tokens
    '''
    tokens=[]
    f = open(fileName)
    for line in f:
        line = line.lower().rstrip()
        for token in line.split(' '):
            if re.match('[0-9]', token):
                pass
            else:
                token = re.sub('\W', '', token)
                tokens.append(token)
    tokens.remove('')
    return tokens


