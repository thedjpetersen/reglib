import utilities

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
        return utilities.login(self.sid, self.pin)

    # This function fetches the transcript page and parses it
    # It sets the classes transcript variable to the transcript class
    def get_transcript(self):
        self.transcript = utilities.get_transcript(self.sid, self.pin)

    # Function to set our schedule variable
    def get_schedule(self):
        self.schedule = utilities.get_schedule(self.sid, self.pin)

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
        return utilities.get_major_requirements(self.sid, self.pin)

    # Function to add class to a schedule
    def add_class(self, crn, crn2=''):
        return utilities.add_class(crn, crn2, self.schedule)

    def get_calendar(self):
        return utilities.get_calendar(self.sid, self.pin, self.schedule.current_term)

