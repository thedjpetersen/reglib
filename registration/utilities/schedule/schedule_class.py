class Schedule(object):
    def __init__(self, html, current_classes, current_term):
       self.current_classes = current_classes
       self.current_term = current_term
       self.schedule = {'Monday':[], 'Tuesday':[], 'Wednesday':[], 'Thursday':[], 'Friday':[]}

       for entry in self.current_classes:
            for day in entry['Days']:
                class_data = [entry['Time'], entry['Location'], (' ').join([entry['Department'], entry['Class Number']]), entry['Type']]
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

    def has_class(self, dep, num):
        for each_class in self.current_classes:
            if each_class['Department'] == dep.upper() and each_class['Class Number'] == num:
                return True
        return False


