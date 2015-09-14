import sys
from bs4 import BeautifulSoup
import urllib
    

def main(fileName):
    outFile = open('outPut.txt', 'w')

    with open(fileName) as f:
        links = f.readlines()

    for link in links:
        html = urllib.urlopen(link).read()
        soup = BeautifulSoup(html)
        # find all paragraph tags in html 
        paragraphs = soup('p')
        for p in paragraphs:
            print >> outFile, p.extract()

if __name__ == "__main__":
    fileName = sys.argv[1]
    main(fileName)
