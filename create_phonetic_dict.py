from tokenize_corpus import tokenize_file
import re

def save_pronunciation_dict(tokens, lookupTable):
    outFile = open('kyrgyz.dict', mode='wt', encoding='utf-8') 

    for token in sorted(set(tokens)):
        phonemes=token

        # palatal/uvular plosives followed by front/back vowels
        phonemes = re.sub(r'к([аоуы])', r'K \1', phonemes)
        phonemes = re.sub(r'к([иеэөү])', r'K \1', phonemes)
        phonemes = re.sub(r'г([аоуы])', r'G \1', phonemes)
        phonemes = re.sub(r'г([иеэөү])', r'G \1', phonemes)

        # syllable final palatal/velar plosives preceded by front/back vowels
        phonemes = re.sub(r'([аоуы])к([^аоуыиеэөү])', r'\1K \2', phonemes)
        phonemes = re.sub(r'([иеэөү])к([^аоуыиеэөү])', r'\1K \2', phonemes)
        phonemes = re.sub(r'([аоуы])г([^аоуыиеэөү])', r'\1G \2', phonemes)
        phonemes = re.sub(r'([иеэөү])г([^аоуыиеэөү])', r'\1G \2', phonemes)

        # word final palatal/velar plosives preceded by front/back vowels
        phonemes = re.sub(r'([аоуы])к($)', r'\1K', phonemes)
        phonemes = re.sub(r'([иеэөү])к($)', r'\1K', phonemes)
        phonemes = re.sub(r'([аоуы])г($)', r'\1G', phonemes)
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
        
        print((token + ' ' + phonemes), end="\n", file=outFile)


# based on Arpabet https://en.wikipedia.org/wiki/Arpabet
lookupTable = {'а':'AA ',
               'о':'OW ',
               'у':'UW ',
               'ы':'IH ',
            
               'и':'IY ',
               'е':'EH ',
               'э':'EH ',
               'ө':'AH ',
               'ү':'UW ',
               
               'ю':'Y UH ',
               'я':'Y AA ',
               'ё':'Y OW ',
               
               'п':'P ',
               'б':'B ',
               
               'д':'D ',
               'т':'T ',

               'к':'K ',
               'г':'G ',
               
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
               'ц':'T S ',
               'ч':'CH ',
               'ф':'F ',
               'в':'V ',
               'х':'HH ',
               'р':'R ',
               'ъ':' ',
               'ь':' '}
        
        
if __name__ == "__main__":
    fileName = input("enter file path here: ")
    tokens = tokenize_file(fileName)
    save_pronunciation_dict(tokens, lookupTable)
