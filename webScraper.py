from bs4 import BeautifulSoup
import urllib
import sys
import time

class Crawler(object):

    def __init__(self, seed):
        self.seed = seed
        self.queuedLinks = [seed]
        self.attemptedLinks = []
        self.outFile = open('outPut.txt', 'w')
        self.strip_links_from_page()

        
    def strip_links_from_page(self):
        while self.queuedLinks:
            time.sleep(.001) 
            # take link off top of stack
            self.currentLink = self.queuedLinks[0]
            print self.currentLink

            # add link to list of queued links
            self.attemptedLinks.append(self.currentLink)
            # remove the link so we don't crawl it again
            del(self.queuedLinks[0])
            
            try:
                # open and read URL
                r = urllib.urlopen(self.currentLink).read()
                # print the link that worked to a file
                print >> self.outFile, self.currentLink
                soup = BeautifulSoup(r)
            except Exception, ex:
                print ex
            
            try:
                # iterate through all links on page
                for link in soup.find_all('a'):
                    print link['href']
                    # just get the url
                    myLink = link['href']
                    
                    # # these are external links
                    # if myLink.startswith('//'):
                    #     pass

                    # # internal links may not have beginning part, so paste it on
                    # if myLink.startswith('/'):
                    #     myLink = seed + myLink
                        
                    # check if we've seen the link already
                    if (myLink in self.attemptedLinks or
                        myLink in self.queuedLinks):
                        pass
                    
                    # check if link starts with the seed URL (internal link)
                    elif myLink.startswith(seed):
                        self.queuedLinks.append(myLink)
            except:
                pass
            
            print 'attempted = ' + str(len(self.attemptedLinks))
            print 'queued = ' + str(len(self.queuedLinks))
            
        

if __name__ == "__main__":
    seed = 'http://' + sys.argv[1]
    C = Crawler(seed)
