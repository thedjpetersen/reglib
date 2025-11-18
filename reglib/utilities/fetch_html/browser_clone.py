import urllib.request
import urllib.parse
import http.cookiejar

header_values = {'User-Agent': 'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16', 'Accept': 'application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding': 'gzip,deflate,sdch', 'Accept-Language': 'en-US,en;q=0.8', 'Cache-Control': 'max-age=0', 'Connection': 'keep-alive', 'Host': 'adminfo.ucsadm.oregonstate.edu', 'Referer': 'https://adminfo.ucsadm.oregonstate.edu/prod/twbkwbis.P_WWWLogin'}

cj = http.cookiejar.MozillaCookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj), urllib.request.HTTPHandler())
urllib.request.install_opener(opener)
