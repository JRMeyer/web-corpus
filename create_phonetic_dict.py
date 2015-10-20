from tokenize_corpus import tokenize_file
import re

def save_pronunciation_dict(tokens, lookupTable):
    outFile = open('output.txt', mode='wt', encoding='utf-8') 

    for token in sorted(set(tokens)):
        phonemes=token

        # palatal/uvular plosives followed by front/back vowels
        phonemes = re.sub(r'к([аоуы])', r'Q \1', phonemes)
        phonemes = re.sub(r'к([иеэөү])', r'K \1', phonemes)
        phonemes = re.sub(r'г([аоуы])', r'GH \1', phonemes)
        phonemes = re.sub(r'г([иеэөү])', r'G \1', phonemes)

        # syllable final palatal/velar plosives preceded by front/back vowels
        phonemes = re.sub(r'([аоуы])к([^аоуыиеэөү])', r'\1Q \2', phonemes)
        phonemes = re.sub(r'([иеэөү])к([^аоуыиеэөү])', r'\1K \2', phonemes)
        phonemes = re.sub(r'([аоуы])г([^аоуыиеэөү])', r'\1GH \2', phonemes)
        phonemes = re.sub(r'([иеэөү])г([^аоуыиеэөү])', r'\1G \2', phonemes)

        # word final palatal/velar plosives preceded by front/back vowels
        phonemes = re.sub(r'([аоуы])к($)', r'\1Q', phonemes)
        phonemes = re.sub(r'([иеэөү])к($)', r'\1K', phonemes)
        phonemes = re.sub(r'([аоуы])г($)', r'\1GH', phonemes)
        phonemes = re.sub(r'([иеэөү])г($)', r'\1G', phonemes)

        # /b/ between back vowels goes to [w] 
        phonemes = re.sub(r'([аоуы])б([аоуы])', r'\1W \2', phonemes)

        # diphthongs
        phonemes = re.sub(r'ой', r'OY ', phonemes)
        phonemes = re.sub(r'ай', r'AY ', phonemes)

        for character in phonemes:
            if character in lookupTable:
                phonemes = re.sub(character, lookupTable[character], phonemes)

        # in case we added a space to the end of the sequence
        phonemes=phonemes.strip()
        
        print((token + '\t' + phonemes), end="\n", file=outFile)


# based on Arpabet https://en.wikipedia.org/wiki/Arpabet
lookupTable = {'а':'AA ',
               'о':'OW ',
               'у':'UW ',
               'ы':'IH ',
            
               'и':'IY ',
               'е':'EH ',
               'э':'EH ',
               'ө':'OE ',
               'ү':'YY ',
               
               'ю':'Y UH ',
               'я':'Y AA ',
               'ё':'Y OW ',
               
               'п':'P ',
               'б':'B ',
               
               'д':'D ',
               'т':'T ',
               
               'ш':'SH ',
               'щ':'SH ',
               'ж':'JH ',
            
               'й':'Y ',
               'л':'L ',
               'м':'M ',
               'н':'N ',
               'ң':'NG ',
               
               'з':'Z ',
               'с':'S ',
               'ц':'TS ',
               'ч':'CH ',
               'ф':'F ',
               'х':'HH ',
               'р':'R '}
        
        
if __name__ == "__main__":
    fileName = input("enter file path here: ")
    tokens = tokenize_file(fileName)
    save_pronunciation_dict(tokens, lookupTable)
