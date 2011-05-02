from urllib2 import urlopen

def advice():
    return urlopen('http://catalog.oregonstate.edu/BCC.aspx').read()
