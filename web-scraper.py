# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib.request as request
import urllib.parse as parse
import http.client as client
import sys
import time
import re
import random
import argparse
import requests
import urllib
import os

class Crawler(object):
    def __init__(self,seed,pluses,minuses,wander,verbose,outfile):
        self.outfile = outfile
        self.seed = seed
        self.projectDir = str(parse.urlsplit(seed).netloc).replace(".","-")
        if not os.path.isdir(self.projectDir):
            os.mkdir(self.projectDir)
        self.wander = wander
        self.verbose = verbose
        self.queuedLinks = set([seed])
        self.attemptedLinks = set()
        self.rejectedLinks = set()
        plusRegex, minusRegex = self.make_regexes_for_scoring(pluses,minuses)
        self.strip_links_from_page(plusRegex,minusRegex)

    def strip_links_from_page(self,plusRegex,minusRegex):
        outfile = open(self.projectDir+"/"+self.outfile, 'w')
        mediaRegex = ('(download(=.+)?|wmv|avi|flv|mov|mkv|mp3|mp4|swf|ra.?|'+
                      'rm|as.|m4[av]|smi.?|jpg|png|pdf|tif|gif|svg|bmp)$')
        mediaRegex = re.compile(mediaRegex)

        i=0
        while self.queuedLinks:
            i+=1
            currentLink = random.sample(self.queuedLinks,1)[0] # take link off top of stack
            print('======================\n', 'Current link : ',currentLink)
            self.attemptedLinks.add(currentLink) # add to list of attempted links
            self.queuedLinks.remove(currentLink) # don't crawl it again

            try:
                # SCRAPE TEXT FROM CURRENT URL
                req = urllib.request.Request(currentLink,headers={'User-Agent': 'Mozilla/5.0'})
                r = urllib.request.urlopen(req, timeout=5).read()
                soup = BeautifulSoup(r, features="html.parser")
                score,text = self.score_page(soup,plusRegex,minusRegex)
                if self.verbose:
                    print('Info: Score of {} for {}'.format(score,currentLink))
                assert (score >0), "currentLink has a score not greater than Zero (0)"
                print(text,file=outfile)
                # SCRAPE LINKS FROM CURRENT URL
                for foundLink in soup.find_all('a'):
                    # first, check if empty link
                    if not 'href' in str(foundLink):
                        if self.verbose:
                            print('R: Empty link : ', foundLink)
                        foundLink = None
                    else:
                        foundLink = foundLink['href']

                    if foundLink and re.search(mediaRegex,foundLink):
                        self.rejectedLinks.add(foundLink)
                        if self.verbose:
                            print('R: Media : ', foundLink)
                        foundLink = None
                    elif foundLink and foundLink.startswith(self.seed):
                        pass
                    elif foundLink and foundLink.startswith('/'):
                        foundLink = urllib.parse.urljoin(currentLink,foundLink)
                    elif foundLink and foundLink.startswith('http'):
                        # link starts with http but not the seed URL
                        self.rejectedLinks.add(foundLink)
                        if self.verbose:
                            print('R: Outsider : ', foundLink)
                        foundLink = None
                    elif foundLink:
                        # some links have missing slashes, so add one
                        foundLink = urllib.parse.urljoin(currentLink,"/"+foundLink)

                    if (not foundLink or foundLink in self.attemptedLinks or
                        foundLink in self.queuedLinks or foundLink in self.rejectedLinks):
                        # pass if we've seen link already or if link == None
                        pass
                    else:
                        self.queuedLinks.add(foundLink)
                        if self.verbose:
                            print('A : ', foundLink)
            except Exception as e:
                print(e)
                pass
            print('attempted = ' + str(len(self.attemptedLinks)))
            print('queued = ' + str(len(self.queuedLinks)))
            print('rejected = ' + str(len(self.rejectedLinks)))

            if i%10000 == 0:
                # save progress to files every 10000 links
                with open(self.projectDir+"/attempted."+str(i)+".txt", "w") as f:
                    print(self.attemptedLinks, file=f)
                with open(self.projectDir+"/queued."+str(i)+".txt", "w") as f:
                    print(self.queuedLinks, file=f)
                with open(self.projectDir+"/rejected."+str(i)+".txt", "w") as f:
                    print(self.rejectedLinks, file=f)

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
        totalPluses = (len(re.findall(plusRegex,text)))
        totalMinuses = (len(re.findall(minusRegex,text)))
        if args.verbose:
            print("Info: totalPluses == {}".format(totalPluses))
            print("Info: totalMinuses == {}".format(totalMinuses))

        if args.strict_voting:
            if (totalPluses == 0) or (totalMinuses > 0):
                score = 0
            else:
                score = totalPluses - totalMinuses
        else:
            score = totalPluses - totalMinuses
        return score,text


def parse_user_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-s','--seed', type=str,help='seed URL for crawller', 
                        required=True)
    parser.add_argument('-w','--wander', action='store_true', default=False, 
                        help='allow crawling on sites other than seed')
    parser.add_argument('-v', '--verbose', action='store_true', default=False, 
                        help='increase output verbosity')
    parser.add_argument('-o','--outfile', type=str,help='where to save output', required=True)
    parser.add_argument('-p','--pluses', type=str,help='comma-separated list of words for upvoting a page', required=True)
    parser.add_argument('-m','--minuses', type=str,help='comma-separated list of words for downvoting a page', required=True)
    parser.add_argument('--strict_voting', action='store_true', default=False, 
                        help='implement strict voting, so that a page must a have "pluses" and cannot have "minuses"')

    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_user_args()

    seed = args.seed
    wander = args.wander
    verbose = args.verbose
    outfile = args.outfile
    pluses=[]
    for plus in args.pluses.split(","):
        pluses.append([plus])
    minuses=[]
    for minus in args.minuses.split(","):
        minuses.append([minus])
    if args.verbose:
        print("Upvoting pages with these words: {}".format(pluses))
        print("Downvoting pages with these words: {}".format(minuses))

    C = Crawler(seed,pluses,minuses,wander,verbose,outfile)
