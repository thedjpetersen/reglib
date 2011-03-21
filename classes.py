import urllib
import urllib2
import cookielib
import transcript 

class Classes:

    #Our header values for the login request
    #make sure that we look like a browser
    header_values =  {'User-Agent' : 'Internet Explorer', 'Accept' : 'application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5', 'Accept-Charset' : 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding' : 'gzip,deflate,sdch', 'Accept-Language' : 'en-US,en;q=0.8', 'Cache-Control' : 'max-age=0', 'Connection' : 'keep-alive', 'Host' : 'adminfo.ucsadm.oregonstate.edu', 'Referer' : 'https://adminfo.ucsadm.oregonstate.edu/prod/twbkwbis.P_WWWLogin'}
    
    def __init__(self, sid, pin):
        #Set up the your identification to be posted when you login
        self.sid = sid
        self.pin = pin

        #Set up a cookie jar to keep the cookies, to keep our session
        self.cj = cookielib.MozillaCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj), urllib2.HTTPHandler())
        urllib2.install_opener(self.opener) 
        #login to set session cookie
        self.login()

    def login(self):
        #Set the referer to appear to be the www login page
        self.header_values['Referer'] = 'https://adminfo.ucsadm.oregonstate.edu/prod/twbkwbis.P_WWWLogin'
        
        #Data to be posted on form
        form_data = urllib.urlencode({'sid' : self.sid, 'PIN' : self.pin})
        #The login url
        login_url = 'https://adminfo.ucsadm.oregonstate.edu/prod/twbkwbis.P_ValLogin'

        #build our request and login to set the SESSID cookie
        request = urllib2.Request(login_url, form_data, headers = self.header_values)
        response = self.opener.open(request)
        if response.headers['Set-Cookie']:
            return True
        return False

    def get_transcript(self):
        #The transcript page url
        trans_url = 'https://adminfo.ucsadm.oregonstate.edu/prod/bwskotrn.P_ViewTran'

        #set up correct header information
        self.header_values['Referer'] = 'https://adminfo.ucsadm.oregonstate.edu/prod/bwskotrn.P_ViewTermTran'
        self.header_values['Origin'] = 'https://adminfo.ucsadm.oregonstate.edu'
        form_data = urllib.urlencode({'levl' : '', 'tprt' : 'WWW'})
        request = urllib2.Request(trans_url, form_data, headers = self.header_values)
        response = self.opener.open(request)
        if response.headers['Set-Cookie']:
            html = response.read()
            return transcript.Transcript(html)
        else:
            login()

    def get_current_classes(self):
        classes_list_url = 'https://adminfo.ucsadm.oregonstate.edu/prod/bwskfshd.P_CrseSchdDetl'
        form_data = urllib.urlencode({'term_in' : '201103'})
        self.header_values['Referer'] = 'https://adminfo.ucsadm.oregonstate.edu/prod/twbkwbis.P_GenMenu?name=bmenu.P_RegMnu'

        request = urllib2.Request(classes_list_url, form_data, headers=self.header_values)
        response = self.opener.open(request)
        return response
