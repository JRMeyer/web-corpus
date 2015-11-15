from bs4 import BeautifulSoup
import urllib
import sys
import time
import re



class Crawler(object):

    def __init__(self,seed,pluses,minuses):
        self.queuedLinks = [seed]
        self.attemptedLinks = []
        self.strip_links_from_page(pluses,minuses)

        
    def strip_links_from_page(self,pluses,minuses):
        outfile = open('output.txt', 'w')

        while self.queuedLinks:
            # take link off top of stack
            self.currentLink = self.queuedLinks[0]

            print('======================')
            print(self.currentLink)

            # add link to list of attempted links
            self.attemptedLinks.append(self.currentLink)

            # remove the link so we don't crawl it again
            del(self.queuedLinks[0])

            if re.match('(download|wmv|avi|flv|mov|mkv|mp..?|swf|ra.?|rm|as.|m4[av]|smi.?)',
                        self.currentLink):
                score=0
            else:
                try:
                    # open and read URL
                    r = urllib.request.urlopen(self.currentLink).read()
                    soup = BeautifulSoup(r)
                    score,text = self.score_page(soup,pluses,minuses)
                    print(score)
                except Exception as exception:
                    print(exception)


            # if the page looks more Kyrgyz than another language
            if score > 0:

                outfile.write(text + '\n')

                try:
                    # iterate through all links on page
                    for tryLink in soup.find_all('a'):
                        tryLink = tryLink['href']

                        # the link is a full URL
                        if tryLink.startswith('http'):
                            pass

                        # internal links, so paste on beginning
                        elif tryLink.startswith('/'):
                            tryLink = urllib.parse.urljoin(self.currentLink,
                                                           tryLink)

                        else:
                            tryLink=None

                        # check if we've seen the link already
                        if (tryLink in self.attemptedLinks or
                            tryLink in self.queuedLinks or tryLink == None):
                            pass
                        else:
                            self.queuedLinks.append(tryLink)
                except:
                    pass

                print('attempted = ' + str(len(self.attemptedLinks)))
                print('queued = ' + str(len(self.queuedLinks)))
            else:
                pass

            
    def score_page(self,soup,pluses,minuses):

        score=0
        text = (' ').join([p.getText() for p in soup.findAll('p')])

        allPluses=[]
        for plus in pluses:
            allPluses+=plus

        allMinuses=[]
        for minus in minuses:
            allMinuses+=minus
            
        # Make regexes which match if any of our regexes match
        plus = "(" + ")|(".join(allPluses) + ")"
        score += (len(re.findall(plus,text)))

        minus = "(" + ")|(".join(allMinuses) + ")"
        score -= (len(re.findall(minus,text)))
        
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




if __name__ == "__main__":
    seed =  sys.argv[1]
    pluses = [kyrgyzWords]
    minuses = [russianWords,kazakhLetters,tajikLetters]
    C = Crawler(seed,pluses,minuses)
