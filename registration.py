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
        self.sid = sid      #this is our student id number
        self.pin = pin      #this is our student pin
        self.login_number = 2       #this variable will be used when we are trying to login

        #Set up a cookie jar to keep the cookies, to keep our session
        self.cj = cookielib.MozillaCookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cj), urllib2.HTTPHandler())
        urllib2.install_opener(self.opener) 
        
        self.login()    #Set the setid cookie
        successful_login = self.login()
        
        #If our users credentials were not correct raise an exception to tell them
        if not successful_login: raise Exception("Invalid credentials")
        self.get_schedule()     #We retrieve our schedule
        self.get_transcript()   #We retrieve our transcript

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
        
        #Test to make sure that our response is not a login failure page
        #Right now testing against length of response, should test against 
        #page title eventually
        if len(response.read())<1000:
            return True
        return False

    # This function fetches the transcript page and parses it
    # It sets the classes transcript variable to the transcript class
    def get_transcript(self):
        for i in range(self.login_number):  #If we are not logged in we will loop around again
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
                # We set the transcript variable to a instance of the transcript class
                self.transcript = transcript.Transcript(html)
            else:
                self.login()

    # Function to set our schedule variable
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
                    self.schedule = schedule.Schedule(html)
            else:
                self.login()
                continue

            form_data = urllib.urlencode({'term_in' : self.current_term})

            request = urllib2.Request(classes_list_url, form_data, headers=self.header_values)
            response = self.opener.open(request)
            html = response.read()
            self.schedule = schedule.Schedule(html)

    # This function searches for classes
    # It can take a term as a parameter as well
    def class_search(self, dep, num, term=''):
        class_url = "http://catalog.oregonstate.edu/CourseDetail.aspx?Columns=abcdfghijklmnopqrstuvwxyz&SubjectCode=" + dep + "&CourseNumber=" + num + "&Campus=corvallis"
        
        response = urllib2.urlopen(class_url)
        if response.url == 'http://catalog.oregonstate.edu/DOE.aspx?Entity=Course':
            return "Class not found"
        html = response.read()

        # Get a array of available classes
        classes = parse_html.class_search(html, dep, num)
        if term is '':
            return classes
        
        # Get classes from certain term
        else:
            list_of_classes = []
            for each_class in classes:
                if each_class['Term'] == term:
                    #If the classes are in a certain term return them
                    list_of_classes.append(each_class)
            if len(list_of_classes) is not 0:
                return list_of_classes
            else:
                return "No classes offered for that term"

    # This function searches for classes that don't conflict with your 
    # current schedule
    def class_search_schedule(self, dep, num):
        terms = {'01':'F', '02':'W', '03':'Sp', '04':'Su'}
        term = terms[self.current_term[-2:]] + self.current_term[2:4]
    
        search_results = self.class_search(dep, num, term)
        # If no classes are found, the function will return a string
        if type(search_results) is str:
            return search_results
        
        available_classes = []

        for result in search_results:
            flag = False
            # If the class is full
            if result['Avail'] <= '0':
                print "Full class"
                continue
            result_days = result['Day/Time/Date']['Days']
            result_times = result['Day/Time/Date']['Time']
            for current_class in self.schedule.current_classes:
                curr_days = current_class['Days']
                curr_time = current_class['Time']
                if(set(result_days).intersection(curr_days)):
                    #If we have a conflict set the flag 
                    if self.time_conflict(result_times, curr_time): 
                        print ('-').join(result_times) + " conflicts with " + ('-').join(curr_time)
                        flag = True
                    else:
                        print ('-').join(result_times) + " does not conflict with " + ('-').join(curr_time)
            if not flag:
                # If no conflict appned to results(flag unset)
                available_classes.append(result)

        return available_classes

    def make_schedule(self, list_of_classes, term = ''):
        class_types = ['Lecture', 'WWW']
        
        if term == '':
            terms = {'01':'F', '02':'W', '03':'Sp', '04':'Su'}
            term = terms[self.current_term[-2:]] + self.current_term[2:4]
        class_search_results = []
        
        for each_class in list_of_classes:
            class_array = each_class.split(' ')
            result_set = self.class_search(class_array[0], class_array[1], term)
            if type(result_set) is not str:
                new_set = [] 
                for index, result in enumerate(result_set):
                    if result['Type'] not in class_types:
                        continue 
                    elif not result['Avail'] > 0: 
                        continue 

                    new_set.append(result)
                    
                class_search_results.append(new_set)

        class_set = []
        combinations = []
        for result_set in class_search_results:
            for result in result_set:
                combinations.append([result])
                for combination in combinations:
                    for member in combination:
                        flag = False
                        if member['Dep'] == result['Dep'] and member['Num'] == result['Num']:
                            flag = True 
                        if self.class_search_conflict(result, member):
                            flag = True 
                    if not flag:
                        combination.append(result)

        return combinations


    def class_search_conflict(self, class1, class2):
        if (set(class1['Day/Time/Date']['Days']).intersection(class2['Day/Time/Date']['Days']) and self.time_conflict(class1['Day/Time/Date']['Time'], class2['Day/Time/Date']['Time'])):
            return True
        return False

    # Helper function that will determine whether or not two times conflict
    # Format of time is ['13:00', '13:50']
    def time_conflict(self, time, time1):
        if (time[0] >= time1[0] and time[0] <= time1[1]) or (time[1] >= time1[0] and time[1] <= time1[1]):
            return True
        return False

    # Function that retrieves the mydegrees page
    def get_major_requirements(self):
        form_page = "https://adminfo.ucsadm.oregonstate.edu/prod/bwykg_dwssbstudent.P_SignOn"
        self.header_values['Referer'] = "https://adminfo.ucsadm.oregonstate.edu/prod/twbkwbis.P_GenMenu?name=bmenu.P_AdminMnu"

        # Get request page for the form
        request = urllib2.Request(form_page, headers = self.header_values)
        response = self.opener.open(request)
        html = response.read()
        form_list = parse_html.mydegrees_redirect_form(html)
        form_data = urllib.urlencode(form_list)

        # Get first page from mydegrees
        mydegrees_url = "https://mydegrees.oregonstate.edu/IRISLink.cgi"
        self.header_values['Referer'] = "https://adminfo.ucsadm.oregonstate.edu/prod/bwykg_dwssbstudent.P_SignOn"
        
        request = urllib2.Request(mydegrees_url, form_data, headers= self.header_values)
        response = self.opener.open(request)

        self.header_values['Referer'] = "https://mydegrees.oregonstate.edu/SD_LoadFrameForm.html"

        form_data = urllib.urlencode({'SERVICE':'SCRIPTER','SCRIPT':'SD2STUCON'})
        request = urllib2.Request(mydegrees_url, form_data, headers = self.header_values)
        response = self.opener.open(request)
        html = response.read() #final form is in html.forms[7].form_values()

        # Get variables from mydegrees
        form_list = parse_html.mydegrees_form_mangler(html)
        form_data = urllib.urlencode(form_list)
        request = urllib2.Request(mydegrees_url, form_data, headers= self.header_values)
        response = self.opener.open(request)
        html = response.read()

        # Get more variables from mydegrees
        form_list = parse_html.mydegrees_final_form(html)
        # Construct variables to post 
        form_data = urllib.urlencode(form_list)
        request = urllib2.Request(mydegrees_url, form_data, headers= self.header_values) 
        # Make request for degree audit xml from mydegrees
        response = self.opener.open(request)
        xml = response.read()
        
        return parse_html.get_major_requirements(xml)

    # Function to add class to a schedule
    def add_class(self, crn, crn2=''):
        for i in range(self.login_number):
            #Page with the form to add/drop classes
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
            
            # Get a dictionary of values to post as the form
            values = parse_html.add_class(html, crn, crn2)
           
            #Set up data to be posted
            form_data = urllib.urlencode(values)
            self.header_values['Referer'] = 'https://adminfo.ucsadm.oregonstate.edu/prod/bwskfreg.P_AltPin'
            submit_url = 'https://adminfo.ucsadm.oregonstate.edu/prod/bwckcoms.P_Regs'

            request = urllib2.Request(submit_url, form_data, headers=self.header_values)
            # Request page with CRNs of classes to add
            response = self.opener.open(request)

            html = response.read()
            
            # See if there were any errors when posting the form
            return parse_html.add_class_has_errors(html) 

