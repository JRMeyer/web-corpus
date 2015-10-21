import re

def tokenize_file(fileName):
    '''
    (1) lower all text 
    (2) strip newlines
    (3) tokenize on whitespace
    (4) throw out numbers
    (5) remove non-alphabetic characters
    (6) return tokens
    '''
    tokens=[]
    f = open(fileName)
    for line in f:
        line = line.lower().rstrip()
        for token in line.split(' '):
            # this number mathcing doesn't seem to work :/
            if re.match(r'[0-9]', token):
                pass
            else:
                token = re.sub(r'\W', r'', token)
                tokens.append(token)
    try:
        # in case we replaced somthing with ''
        tokens.remove('')
    except:
        pass
    
    return tokens


