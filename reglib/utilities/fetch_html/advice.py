from urllib.request import urlopen

def advice():
    return urlopen('http://catalog.oregonstate.edu/BCC.aspx').read()
