import sys
from bs4 import BeautifulSoup, element
import urllib

# might come in handy later
def visible(myElement):
    '''
    check each element from a page and check if it's visible text
    '''
    if myElement.parent.name in ['style', 'script', '[document]', 'head',
                               'title']:
        return False
    elif isinstance(element, element.Comment):
        return False
    else:
        return True
    

def main(fileName):
    outFile = open('outPut.txt', 'w')

    with open(fileName) as f:
        links = f.readlines()

    for link in links:
        html = urllib.urlopen(link).read()
        soup = BeautifulSoup(html)
        # find all paragraph tags in html and print to file
        print >> outFile, soup("p")


if __name__ == "__main__":
    fileName = sys.argv[1]
    main(fileName)
