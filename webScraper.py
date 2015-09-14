from bs4 import BeautifulSoup
import urllib
import sys
from send_email import *
import time

class Crawler(object):

    def __init__(self, seed):
        self.seed = seed
        self.potentialLinks = [seed]
        self.attemptedLinks = []
        self.outFile = open('outPut.txt', 'w')
        self.strip_links_from_page()

        
    def strip_links_from_page(self):
        while self.potentialLinks:
            time.sleep(1) 
            # take link off top of stack
            self.currentLink = self.potentialLinks[0]
            self.attemptedLinks.append(self.currentLink)
            # remove the link so we don't crawl it again
            del(self.potentialLinks[0])
            
            try:
                # open and read URL
                r = urllib.urlopen(self.currentLink).read()
                # print the link that worked to a file
                print >> self.outFile, self.currentLink
                soup = BeautifulSoup(r)
            except Exception, ex:
                print ex
                pass
            
            try:
                # iterate through all links on page
                for link in soup.find_all('a'):
                    # check if link starts with the seed URL
                    if link.get('href').startswith(seed):
                        self.potentialLinks.append(link['href'])
                    # link doesnt contain seed, begins with http == different site
                    elif link.get('href').startswith('http://'):
                        pass
                    # internal links do not have beginning part, so paste it on
                    elif link.get('href').startswith('/'):
                        self.potentialLinks.append(seed+link['href'])
                    # make sure not to add a duplicate link
                    self.potentialLinks = self.remove_duplicates(
                        self.potentialLinks)
            except:
                pass
            
            print self.currentLink
            print 'attempted = ' + str(len(self.attemptedLinks))
            print 'potential = ' + str(len(self.potentialLinks))
            
        # send_email('joshua.richard.meyer@gmail.com', 'fooDir')

        
    def remove_duplicates(self, sequence):
        ''' remove duplicates from list and preserve order '''
        return [x for x in set(sequence) if not (x in self.attemptedLinks)]
        # seen = set()
        # seen_add = seen.add
        # return [x for x in sequence if not (x in seen or seen_add(x) or
        #                                     x in self.attemptedLinks)]
    
if __name__ == "__main__":
    seed = 'http://' + sys.argv[1]
    C = Crawler(seed)
