class Schedule(object):
    """ dictionary with days as key and course list as values """

    def __init__(self, html, current_classes, current_term):
       """ gets list of current courses and returns as a dictionary
       with days as the key and courses as the values """

       self.current_classes = current_classes
       self.current_term = current_term
       self.schedule = {'Monday':[], 'Tuesday':[], 'Wednesday':[], 'Thursday':[], 'Friday':[]}

       for entry in self.current_classes:
            for day in entry['days']:
                class_data = [entry['times'], entry['location'], (' ').join([entry['department'], entry['number']]), entry['type']]
                if day == 'M':
                    self.schedule['Monday'].append(class_data)
                if day == 'T':
                    self.schedule['Tuesday'].append(class_data)
                if day == 'W':
                    self.schedule['Wednesday'].append(class_data)
                if day == 'R':
                    self.schedule['Thursday'].append(class_data)
                if day == 'F':
                    self.schedule['Friday'].append(class_data)
            
            for day in self.schedule:
                self.schedule[day].sort()

    def has_class(self, department, number):
        """ returns true/false whether course is in schedule """

        for each_class in self.current_classes:
            if each_class['department'] == department.upper() and each_class['number'] == number:
                return True
        return False


