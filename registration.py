import fetch_html
import parse_html
import transcript 
import schedule

class infosu(object):

    def __init__(self, sid, pin):
        #Set up the your identification to be posted when you login
        self.sid = sid      #this is our student id number
        self.pin = pin      #this is our student pin
        self.login_number = 2       #this variable will be used when we are trying to login
        
        self.login()    #Set the setid cookie
        successful_login = self.login()
        
        #If our users credentials were not correct raise an exception to tell them
        if not successful_login: raise Exception("Invalid credentials")
        self.get_schedule()     #We retrieve our schedule
        self.get_transcript()   #We retrieve our transcript

    def login(self):
        if len(fetch_html.login(self.sid, self.pin))<1000:
            return True
        return False

    # This function fetches the transcript page and parses it
    # It sets the classes transcript variable to the transcript class
    def get_transcript(self):
        for i in range(self.login_number):  #If we are not logged in we will loop around again
            #The transcript page url
            html = fetch_html.get_transcript()
            
            if parse_html.get_page_title(html) != 'Login':
                # We set the transcript variable to a instance of the transcript class
                grades = parse_html.get_grades(html)
                credits = parse_html.get_total_credits(html)
                self.transcript = transcript.Transcript(html, grades, credits)
            else:
                self.login()

    # Function to set our schedule variable
    def get_schedule(self):
        for i in range(self.login_number):
            
            html = fetch_html.setup_schedule_page()
            title = parse_html.get_page_title(html)
            if title != 'Login':
                if title == 'Select Term ':
                    self.current_term = parse_html.get_current_term(html)
                else:
                    current_classes = parse_html.get_current_classes(html) 
                    self.schedule = schedule.Schedule(html, current_classes)
            else:
                self.login()
                continue

            html = fetch_html.get_schedule(self.current_term)
            current_classes = parse_html.get_current_classes(html)
            self.schedule = schedule.Schedule(html, current_classes)

    # This function searches for classes
    # It can take a term as a parameter as well
    def class_search(self, dep, num, term=''):
        
        html = fetch_html.class_search(dep, num)
        if not html:
            return "Class not found"

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
        html = fetch_html.infosu_mydegrees_redirect()

        form_list = parse_html.mydegrees_redirect_form(html)
        html = fetch_html.first_page_set_cookie(form_list)

        # Get variables from mydegrees
        form_list = parse_html.mydegrees_form_mangler(html)
        html = fetch_html.form_variables(form_list)

        # Get more variables from mydegrees
        form_list = parse_html.mydegrees_final_form(html)
        xml = fetch_html.get_xml(form_list)

        return parse_html.get_major_requirements(xml)

    # Function to add class to a schedule
    def add_class(self, crn, crn2=''):
        for i in range(self.login_number):
            html = fetch_html.setup_ad_page()
            title = parse_html.get_page_title(html)
            form_data = ''
            if title != 'Login':
                if title == 'Select Term ':
                    self.current_term = parse_html.get_current_term(html)
                    form_data = fetch_html.current_term_form(self.current_term)
            else:
                self.login()
                continue
            
            html = fetch_html.add_drop_page(form_data)
            # Get a dictionary of values to post as the form
            values = parse_html.add_class(html, crn, crn2)
            html = fetch_html.add_class(values)
            
            # See if there were any errors when posting the form
            return parse_html.add_class_has_errors(html) 

