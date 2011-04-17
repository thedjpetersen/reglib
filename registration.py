import urllib
import urllib2
import cookielib
import parse_html
import transcript 
import schedule

class infosu(object):

    #Our header values for the login request
    #make sure that we look like a browser
    header_values =  {'User-Agent' : 'Mozilla/5.0 (X11; U; Linux i686 (x86_64); en-US; rv:1.9.2.16) Gecko/20110319 Firefox/3.6.16', 'Accept' : 'application/xml,application/xhtml+xml,text/html;q=0.9,text/plain;q=0.8,image/png,*/*;q=0.5', 'Accept-Charset' : 'ISO-8859-1,utf-8;q=0.7,*;q=0.3', 'Accept-Encoding' : 'gzip,deflate,sdch', 'Accept-Language' : 'en-US,en;q=0.8', 'Cache-Control' : 'max-age=0', 'Connection' : 'keep-alive', 'Host' : 'adminfo.ucsadm.oregonstate.edu', 'Referer' : 'https://adminfo.ucsadm.oregonstate.edu/prod/twbkwbis.P_WWWLogin'}
    
    def __init__(self, sid, pin):
        #Set up the your identification to be posted when you login
        self.sid = sid
        self.pin = pin
        self.login_number = 2

        #Set up a cookie jar to keep the cookies, to keep our session
        self.cj = cookielib.MozillaCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj), urllib2.HTTPHandler())
        urllib2.install_opener(self.opener) 
        
        self.login()    #Set the setid cookie
        successful_login = self.login()

        if not successful_login: raise Exception("Invalid credentials")
        self.get_schedule()
        self.get_transcript()

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
        if len(response.read())<1000:
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

    def get_schedule(self):
        for i in range(self.login_number):
            classes_list_url = 'https://adminfo.ucsadm.oregonstate.edu/prod/bwskfshd.P_CrseSchdDetl'
            self.header_values['Referer'] = 'https://adminfo.ucsadm.oregonstate.edu/prod/twbkwbis.P_GenMenu?name=bmenu.P_RegMnu'

            request = urllib2.Request(classes_list_url, headers = self.header_values)
            response = self.opener.open(request)
            html = response.read()
            title = parse_html.get_page_title(html)
            if title != 'Login':
                if title == 'Select Term ':
                    self.current_term = parse_html.get_current_term(html)
                else:
                    return schedule.Schedule(html)
            else:
                self.login()
                continue

            form_data = urllib.urlencode({'term_in' : self.current_term})

            request = urllib2.Request(classes_list_url, form_data, headers=self.header_values)
            response = self.opener.open(request)
            html = response.read()
            self.schedule = schedule.Schedule(html)

    def update_schedule(self):
        self.get_schedule()

    def class_search(self, dep, num, term=''):
        class_url = "http://catalog.oregonstate.edu/CourseDetail.aspx?Columns=abcdfghijklmnopqrstuvwxyz&SubjectCode=" + dep + "&CourseNumber=" + num + "&Campus=corvallis"
        
        response = urllib2.urlopen(class_url)
        if response.url == 'http://catalog.oregonstate.edu/DOE.aspx?Entity=Course':
            return "Class not found"
        html = response.read()
        classes = parse_html.class_search(html)
        if term is '':
            return classes
        else:
            list_of_classes = []
            for each_class in classes:
                if each_class['Term'] == term:
                    list_of_classes.append(each_class)
                if len(list_of_classes) is not 0:
                    return list_of_classes
                else:
                    return "No classes offered for that term"

    def class_search_schedule(self, dep, num):
        terms = {'01':'F', '02':'W', '03':'Sp', '04':'Su'}
        term = terms[self.current_term[-2:]] + self.current_term[2:4]
    
        search_results = self.class_search(dep, num, term)
        if type(search_results) is str:
            return search_results
        
        available_classes = []

        for result in search_results:
            flag = False
            if result['Avail'] == '0':
                print "Full class"
                continue
            result_days = result['StartDate']['Days']
            result_times = result['StartDate']['Time']
            for current_class in self.schedule.current_classes:
                curr_days = current_class['Days']
                curr_time = current_class['Time']
                if(set(result_days).intersection(curr_days)):
                    if self.conflict(result_times, curr_time): 
                        print ('-').join(result_times) + " conflicts with " + ('-').join(curr_time)
                        flag = True
                    else:
                        print ('-').join(result_times) + " does not conflict with " + ('-').join(curr_time)
            if not flag:
                available_classes.append(result)

        return available_classes

    def conflict(self, time, time1):
        if (time[0] >= time1[0] and time[0] <= time1[1]) or (time[1] >= time1[0] and time[1] <= time1[1]):
            return True
        return False

    def get_major_requirements(self):
        form_page = "https://adminfo.ucsadm.oregonstate.edu/prod/bwykg_dwssbstudent.P_SignOn"
        self.header_values['Referer'] = "https://adminfo.ucsadm.oregonstate.edu/prod/twbkwbis.P_GenMenu?name=bmenu.P_AdminMnu"

        request = urllib2.Request(form_page, headers = self.header_values)
        response = self.opener.open(request)
        html = response.read()
        form_list = parse_html.mydegrees_redirect_form(html)
        form_data = urllib.urlencode(form_list)

        mydegrees_url = "https://mydegrees.oregonstate.edu/IRISLink.cgi"
        self.header_values['Referer'] = "https://adminfo.ucsadm.oregonstate.edu/prod/bwykg_dwssbstudent.P_SignOn"
        
        request = urllib2.Request(mydegrees_url, form_data, headers= self.header_values)
        response = self.opener.open(request)

        self.header_values['Referer'] = "https://mydegrees.oregonstate.edu/SD_LoadFrameForm.html"

        form_data = urllib.urlencode({'SERVICE':'SCRIPTER','SCRIPT':'SD2STUCON'})
        #phase one give your data bitch
        request = urllib2.Request(mydegrees_url, form_data, headers = self.header_values)
        response = self.opener.open(request)
        html = response.read() #final form is in html.forms[7].form_values()

        form_list = parse_html.mydegrees_form_mangler(html)
        form_data = urllib.urlencode(form_list)
        request = urllib2.Request(mydegrees_url, form_data, headers= self.header_values)
        response = self.opener.open(request)
        html = response.read()

        form_list = parse_html.mydegrees_final_form(html)
        form_data = urllib.urlencode(form_list)
        request = urllib2.Request(mydegrees_url, form_data, headers= self.header_values) 

        response = self.opener.open(request)
        xml = response.read()
        
        return parse_html.get_major_requirements(xml)

    def add_class(self, crn, crn2=''):
        for i in range(self.login_number):
            add_drop_page_url = 'https://adminfo.ucsadm.oregonstate.edu/prod/bwskfreg.P_AltPin'
            self.header_values['Referer'] = 'https://adminfo.ucsadm.oregonstate.edu/prod/twbkwbis.P_GenMenu?name=bmenu.P_RegMnu'
            request = urllib2.Request(add_drop_page_url, headers = self.header_values)
            response = self.opener.open(request)
            
            html = response.read()
            title = parse_html.get_page_title(html)
            form_data = ''
            if title != 'Login':
                if title == 'Select Term ':
                    self.current_term = parse_html.get_current_term(html)
                    form_data = urllib.urlencode({'term_in' : current_term})
            else:
                self.login()
                continue

            request = urllib2.Request(add_drop_page_url, form_data, headers=self.header_values)
            response = self.opener.open(request)
            html = response.read()
            
            values = parse_html.add_class(html, crn, crn2)
           
            form_data = urllib.urlencode(values)
            self.header_values['Referer'] = 'https://adminfo.ucsadm.oregonstate.edu/prod/bwskfreg.P_AltPin'
            submit_url = 'https://adminfo.ucsadm.oregonstate.edu/prod/bwckcoms.P_Regs'

            request = urllib2.Request(submit_url, form_data, headers=self.header_values)
            response = self.opener.open(request)

            html = response.read()
            
            return parse_html.add_class_has_errors(html) 

