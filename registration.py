import urllib
import urllib2
import cookielib
import parse_html
import transcript 

class infosu:

    #Our header values for the login request
    #make sure that we look like a browser
    header_values =  {'User-Agent' : 'Internet Explorer', 'Accept' : 'application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5', 'Accept-Charset' : 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding' : 'gzip,deflate,sdch', 'Accept-Language' : 'en-US,en;q=0.8', 'Cache-Control' : 'max-age=0', 'Connection' : 'keep-alive', 'Host' : 'adminfo.ucsadm.oregonstate.edu', 'Referer' : 'https://adminfo.ucsadm.oregonstate.edu/prod/twbkwbis.P_WWWLogin'}
    
    def __init__(self, sid, pin):
        #Set up the your identification to be posted when you login
        self.sid = sid
        self.pin = pin
        self.login_number = 2

        #Set up a cookie jar to keep the cookies, to keep our session
        self.cj = cookielib.MozillaCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj), urllib2.HTTPHandler())
        urllib2.install_opener(self.opener) 
        

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
        for i in range(self.login_number):
            #The transcript page url
            trans_url = 'https://adminfo.ucsadm.oregonstate.edu/prod/bwskotrn.P_ViewTran'

            #set up correct header information
            self.header_values['Referer'] = 'https://adminfo.ucsadm.oregonstate.edu/prod/bwskotrn.P_ViewTermTran'
            self.header_values['Origin'] = 'https://adminfo.ucsadm.oregonstate.edu'
            form_data = urllib.urlencode({'levl' : '', 'tprt' : 'WWW'})
            request = urllib2.Request(trans_url, form_data, headers = self.header_values)
            response = self.opener.open(request)
            html = response.read()
            if parse_html.get_page_title(html) != 'Login':
                return transcript.Transcript(html)
            else:
                self.login()

    def get_current_classes(self):
        for i in range(self.login_number):
            classes_list_url = 'https://adminfo.ucsadm.oregonstate.edu/prod/bwskfshd.P_CrseSchdDetl'
            self.header_values['Referer'] = 'https://adminfo.ucsadm.oregonstate.edu/prod/twbkwbis.P_GenMenu?name=bmenu.P_RegMnu'

            request = urllib2.Request(classes_list_url, headers = self.header_values)
            response = self.opener.open(request)
            html = response.read()
            title = parse_html.get_page_title(html)
            if title != 'Login':
                if title == 'Select Term ':
                    current_term = parse_html.get_current_term(html)
                else:
                    return parse_html.get_current_classes(html)
            else:
                self.login()
                continue

            form_data = urllib.urlencode({'term_in' : current_term})

            request = urllib2.Request(classes_list_url, form_data, headers=self.header_values)
            response = self.opener.open(request)
            html = response.read()
            return parse_html.get_current_classes(html)
