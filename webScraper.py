from bs4 import BeautifulSoup
import urllib
import sys
import time
import re



class Crawler(object):

    def __init__(self,seed,kyrgyzWords,russianWords,kazakhLetters,latinLetters,
                 tajikLetters):
        self.queuedLinks = [seed]
        self.attemptedLinks = []
        self.strip_links_from_page(kyrgyzWords,russianWords,kazakhLetters,
                                   latinLetters,tajikLetters)

        
    def strip_links_from_page(self,kyrgyzWords,russianWords,kazakhLetters,
                              latinLetters,tajikLetters):
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

            if 'download' in self.currentLink:
                score=0
            else:
                try:
                    # open and read URL
                    r = urllib.request.urlopen(self.currentLink).read()
                    soup = BeautifulSoup(r)
                    score,text = self.score_page(soup,kyrgyzWords,russianWords,
                                            kazakhLetters,latinLetters,
                                                 tajikLetters)
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

            
    def score_page(self, soup, kyrgyzWords, russianWords, kazakhLetters,
                       latinLetters,tajikLetters):

        score=0
        text = (' ').join([p.getText() for p in soup.findAll('p')])

        # Make regexes which match if any of our regexes match
        kyrgyz = "(" + ")|(".join(kyrgyzWords) + ")"
        score += (len(re.findall(kyrgyz,text)))

        latin = "(" + ")|(".join(latinLetters) + ")"
        score -= (len(re.findall(latin,text)))/10

        kazakh = "(" + ")|(".join(kazakhLetters) + ")"
        score -= (len(re.findall(kazakh,text)))

        tajik = "(" + ")|(".join(tajikLetters) + ")"
        score -= (len(re.findall(tajik,text)))

        russian = "(" + ")|(".join(russianWords) + ")"
        score -= (len(re.findall(russian,text)))
        
        return score,text


kyrgyzWords = {' бирок ',' ооба ',' жок ',' жана ',' менен ',
               ' сен ',' мен ',' бир ',' ал ',' алар ',
               ' анын ',' бул ',' болуп ',' эле ',' боюнча ',
               ' үчүн ',' деп ',' башка ',' ар ',' пайда ',
               ' болот ',' мамлекеттик ',' болгон ',
               ' деген ',' көп '}

russianWords = {' и ',' в ',' не ',' что ',' на ', 
                ' быть ',' я ',' с ',' он ',' а ', 
                ' это ',' так ',' то ',' этот ', 
                ' они ',' мы ',' по ',' к ',' но ', 
                ' она ',' у ',' который ',' весь ', 
                ' из ',' вы ',' так '}

kazakhLetters = {'һ','ғ','қ','ә','ұ','і','ъ'}

latinLetters = {'a','b','c','d','e',
                'f','g','h','i','j',
                'k','l','m','n','o',
                'p','q','r','s','t',
                'u','v','w','x','y',
                'z'}

tajikLetters={'ӣ','ӯ','ҳ','ҷ'}




if __name__ == "__main__":
    seed =  'http://' + sys.argv[1]
    C = Crawler(seed,kyrgyzWords,russianWords,kazakhLetters,latinLetters,
                tajikLetters)
