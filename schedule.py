import parse_html

class Schedule(object):
    def __init__(self, html):
       self.current_classes = parse_html.get_current_classes(html) 
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


