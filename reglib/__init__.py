import utilities

class infosu(object):

    def __getattribute__(self, name):
        try:
            return object.__getattribute__(self,name)
        except AttributeError:
            if name == 'schedule':
                self.get_current_schedule()
                return self.schedule 
            if name == 'transcript':
                self.get_transcript()
                return self.transcript
            if name == 'audit':
                self.get_major_requirements()
                return self.audit
            if name =='next_schedule':
                self.get_next_schedule() 
                return self.next_schedule   

            raise

    def __init__(self, sid, pin, lazy_load=True):
        #Set up the your identification to be posted when you login
        self.sid = sid      #this is our student id number
        self.pin = pin      #this is our student pin
        self.login_number = 2       #this variable will be used when we are trying to login
        
        self.login()    #Set the setid cookie
        successful_login = self.login()
        
        #If our users credentials were not correct raise an exception to tell them
        if not successful_login: raise Exception("Invalid credentials")
        if not lazy_load:
            self.get_current_schedule()     #We retrieve our schedule
            self.get_transcript()   #We retrieve our transcript self.get_next_schedule()
            self.get_major_requirements()
            self.get_next_schedule()

    def login(self):
        return utilities.login(self.sid, self.pin)

    # This function fetches the transcript page and parses it
    # It sets the classes transcript variable to the transcript class
    def get_transcript(self):
        self.transcript = utilities.get_transcript(self.sid, self.pin)

    # Function to set our schedule variable
    def get_current_schedule(self):
        # login again to make sure we can select a different term
        self.login() 
        self.login() 
        self.schedule = utilities.get_schedule(self.sid, self.pin, False)

    # get schedule for next term
    def get_next_schedule(self):
        # login again to make sure we can select a different term
        self.login() 
        self.login() 
        self.next_schedule = utilities.get_schedule(self.sid, self.pin, True) 

    # This function searches for classes
    # It can take a term as a parameter as well
    def class_search(self, dep, num, term=''):
        return utilities.class_search(dep, num, term)

    # This function searches for classes that don't conflict with your 
    # current schedule
    def class_search_schedule(self, dep, num):
        return utilities.class_search_schedule(dep, num, self.schedule)
        
    def make_schedule(self, list_of_classes, term = ''):
        return utilities.make_schedule(list_of_classes, term, self.schedule)

    def class_search_conflict(self, class1, class2):
        return utilities.class_search_conflict(class1, class2)

    # Helper function that will determine whether or not two times conflict
    # Format of time is ['13:00', '13:50']
    def time_conflict(self, time, time1):
        return utilities.time_conflict(time, time1)

    # Function that retrieves the mydegrees page
    def get_major_requirements(self):
        self.audit = utilities.get_major_requirements(self.sid, self.pin)

    # Function to add class to a schedule
    def add_class(self, crn1, crn2=''):
        return utilities.add_class(self.sid, self.pin, crn1, crn2, self.schedule)
    
    # add multiple courses via list, lecture/lab-rec pairs list within the list
    def add_classes(self, crn_list):
        return utilities.add_classes(self.sid, self.pin, crn_list, self.schedule)

    # drop a course
    def drop_classes(self, crn_list):
        return utilities.drop_classes(self.sid, self.pin, crn_list, self.schedule)
        
    


