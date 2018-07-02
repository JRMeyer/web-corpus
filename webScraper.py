from bs4 import BeautifulSoup
import urllib.request
import sys
import time
import re
import random
import argparse

class Crawler(object):

    def __init__(self,seed,pluses,minuses,wander,verbose):
        self.seed = seed
        self.wander = wander
        self.verbose = verbose
        self.queuedLinks = set()
        self.queuedLinks.add(seed)
        self.attemptedLinks = set()
        plusRegex, minusRegex = self.make_regexes_for_scoring(pluses,minuses)
        self.strip_links_from_page(plusRegex,minusRegex)
        
    def strip_links_from_page(self,plusRegex,minusRegex):
        outfile = open('output.txt', 'w')
        mediaRegex = ('(download(=.+)?|wmv|avi|flv|mov|mkv|mp..?|swf|ra.?|'+
                      'rm|as.|m4[av]|smi.?|jpg|png|pdf|tif|gif|svg|bmp)$')
        mediaRegex = re.compile(mediaRegex)
        
        while self.queuedLinks:
            # take link off top of stack
            currentLink = random.sample(self.queuedLinks,1)[0]

            print('======================')
            print('Current link : ',currentLink)

            # add link to list of attempted links
            self.attemptedLinks.add(currentLink)

            # remove the link so we don't crawl it again
            self.queuedLinks.remove(currentLink)

            if re.search(mediaRegex,currentLink):
                print('MEDIA')
                score=0
            else:
                try:
                    # open and read URL
                    req = urllib.request.Request(currentLink,headers={'User-Agent': 'Mozilla/5.0'})
                    r = urllib.request.urlopen(req, timeout=5).read()
                    soup = BeautifulSoup(r)
                    score,text = self.score_page(soup,plusRegex,minusRegex)

                    #r = urllib.request.urlopen(currentLink,timeout=5).read()
                    #soup = BeautifulSoup(r)
                    #score,text = self.score_page(soup,plusRegex,minusRegex)
                    print('Score =', str(score))
                except Exception as exception:
                    print(exception)
                    exit()

            # if the page looks more Kyrgyz than another language
            if score > 0:
                # output the scraped text to file
                outfile.write(text + '\n')
                try:
                    # iterate through all links on page
                    for foundLink in soup.find_all('a'):
                        foundLink = foundLink['href']

                        # if the link is a full URL, just pass it along
                        if foundLink.startswith('http'):
                            pass
                        # else if the link is internal, paste on beginning part
                        elif foundLink.startswith('/'):
                            foundLink = urllib.parse.urljoin(currentLink,
                                                             foundLink)
                        # if it's not a full or internal link, ignore it
                        else:
                            foundLink = None

                        # if we don't want to visit pages besides the seed
                        # and if the found link does not begin with seed...
                        if self.wander == False and foundLink != None:
                            if not foundLink.startswith(self.seed):
                                # foundLink comes from the outside
                                if self.verbose:
                                    print('Outsider rejected! : ', foundLink)
                                foundLink = None
                            else:
                                pass

                        # check if we've seen link already or if link == None
                        if (foundLink in self.attemptedLinks or
                            foundLink in self.queuedLinks or foundLink == None):
                            pass
                        # if it's a new, legitimate link, queue it for later
                        else:
                            self.queuedLinks.add(foundLink)
                            if self.verbose:
                                print('Link kept! : ', foundLink)
                except:
                    pass

                print('attempted = ' + str(len(self.attemptedLinks)))
                print('queued = ' + str(len(self.queuedLinks)))
            else:
                pass

    def make_regexes_for_scoring(self,pluses,minuses):
        # concatenate all lists for scoring text
        allPluses=[]
        for plus in pluses:
            allPluses+=plus
        allMinuses=[]
        for minus in minuses:
            allMinuses+=minus
        # Make regexes which match if any of our regexes match
        plusRegex = re.compile("(" + ")|(".join(allPluses) + ")")
        minusRegex = re.compile("(" + ")|(".join(allMinuses) + ")")
        
        return plusRegex, minusRegex

    def score_page(self,soup,plusRegex,minusRegex):
        # get all 'p' paragraphs from page and paste them into one long string
        text = (' ').join([p.getText() for p in soup.findAll('p')])
        # score page
        score = 0
        score += (len(re.findall(plusRegex,text)))
        score -= (len(re.findall(minusRegex,text)))
        
        return score,text


kyrgyzWords = [' бирок ',' ооба ',' жок ',' жана ',' менен ',
               ' сен ',' мен ', ' сиз ',' ал ',' алар ',
               ' анын ',' бул ',' болуп ',' эле ',' боюнча ',
               ' үчүн ',' деп ',' башка ',' ар ',' пайда ',
               ' болот ',' мамлекеттик ',' болгон ',
               ' деген ',' көп ',' бир ']

russianWords = [' и ',' в ',' не ',' что ',' на ', 
                ' быть ',' я ',' с ',' он ',' а ', 
                ' это ',' так ',' то ',' этот ', 
                ' они ',' мы ',' по ',' к ',' но ', 
                ' она ',' у ',' который ',' весь ', 
                ' из ',' вы ',' так ']

kazakhLetters = ['һ','ғ','қ','ә','ұ','і','ъ']

latinLetters = ['a','b','c','d','e',
                'f','g','h','i','j',
                'k','l','m','n','o',
                'p','q','r','s','t',
                'u','v','w','x','y',
                'z']

tajikLetters = ['ӣ','ӯ','ҳ','ҷ']



def parse_user_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--seed', type=str,help='seed URL for crawller', 
                        required=True)
    parser.add_argument('-w','--wander', action='store_true', default=False, 
                        help='allow crawling on sites other than seed')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, 
                        help='increase output verbosity')
    args = parser.parse_args()
    return args

if __name__ == "__main__":
    args = parse_user_args()

    seed = args.seed
    wander = args.wander
    verbose = args.verbose

    pluses = [kyrgyzWords]
    minuses = [russianWords,kazakhLetters,tajikLetters]
    C = Crawler(seed,pluses,minuses,wander,verbose)
