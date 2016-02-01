# webScraper.py

This script runs on Python 3, so check if you have Python 3 installed with
something like this:
python3 --version

If you have a linux distro, I think it will likely be installed already, but 
if you're using Mac, you can get Python 3 with brew:
brew install python3

On Windows, I'm not sure... let me know if it you get it to work and how 
you did it, and I'll put that info here:)

Once you have Python 3, You need to install BeautifulSoup for Python 3:

Ubuntu has a stable version you can get with this:
sudo apt-get install python3-bs4
Or you can probably try pip3, brew, or easy_install for unix systems.

## USAGE

There are three flags you can feed the script:

python3 webScraper.py -s/--seed -w/--wander -v/--verbose

--seed is a requirement

--wander will let your crawler visit pages which are not children of the seed URL

--verbose will print out to the terminal which URLs were accepted or rejected
