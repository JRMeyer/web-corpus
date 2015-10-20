from tokenize_corpus import tokenize_file
import re

def save_pronunciation_dict(tokens, lookupTable):
    outFile = open('output.txt', mode='wt', encoding='utf-8') 

    for token in sorted(set(tokens)):
        phonemes=token

        # palatal/uvular plosives followed by front/back vowels
        phonemes = re.sub(r'к([аоуы])', r'q \1', phonemes)
        phonemes = re.sub(r'к([иеэөү])', r'k \1', phonemes)
        
        phonemes = re.sub(r'г([аоуы])', r'gh \1', phonemes)
        phonemes = re.sub(r'г([иеэөү])', r'g \1', phonemes)

        # syllable final palatal/velar plosives preceded by front/back vowels
        phonemes = re.sub(r'([аоуы])к([^аоуыиеэөү])', r'\1q \2', phonemes)
        phonemes = re.sub(r'([иеэөү])к([^аоуыиеэөү])', r'\1k \2', phonemes)

        phonemes = re.sub(r'([аоуы])г([^аоуыиеэөү])', r'\1gh \2', phonemes)
        phonemes = re.sub(r'([иеэөү])г([^аоуыиеэөү])', r'\1g \2', phonemes)

        # /b/ between back vowels goes to [w] 
        phonemes = re.sub(r'([аоуы])б([аоуы])', r'\1w \2', phonemes)

        for character in phonemes:
            if character in lookupTable:
                phonemes = re.sub(character, lookupTable[character], phonemes)

        # in case we added a space to the end of the sequence
        phonemes=phonemes.strip()
        
        print((token + '\t' + phonemes), end="\n", file=outFile)


lookupTable = {'а':'a ',
          'о':'o ',
          'у':'u ',
          'ы':'ih ',
          
          'и':'i ',
          'е':'e ',
          'э':'eh ',
          'ө':'oe ',
          'ү':'y ',
          
          'ю':'j u ',
          'я':'j a ',
          'ё':'j o ',
          
          'п':'p ',
          'б':'b ',
          
          'д':'d ',
          'т':'t ',
          
          'ш':'sh ',
          'щ':'sh ',
          'ж':'zh ',
          
          'й':'j ',
          'л':'l ',
          'м':'m ',
          'н':'n ',
          'ң':'ng ',
          
          'з':'z ',
          'с':'s ',
          'ц':'ts ',
          'ч':'tsh ',
          'ф':'f ',
          'х':'h ',
          'р':'r '}
        
        
if __name__ == "__main__":
    fileName = input("enter file path here: ")
    tokens = tokenize_file(fileName)
    save_pronunciation_dict(tokens, lookupTable)
