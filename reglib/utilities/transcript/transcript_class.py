class Transcript(object):
    """ course transcript includes list of classes taken, grades, # credits, gpa """

    def __init__(self, html, grades, credits, gpa):
        self.grades = grades
        self.credits = credits # dictionary (institution, transfer, overall) 
        self.gpa = gpa # dictionary (osu ,transfer)

    def has_class(self, department, number):
        """ returns true/false whether class has been taken regardless of passing """

        number = number.upper()
        department = department.upper()
        for entry in self.grades:
            if entry['department'] == department and entry['number'] == number:
                return True
        return False

    def has_passed_class(self, department, number):
        """ returns true/false whether a pass has been classed (c and above) """

        number = number.upper()
        department = department.upper()
        passing_grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']
        for entry in self.grades:
            if entry['department'] == department and entry['number'] == number and entry['grade'] in passing_grades:
                return True
        return False

    def grade_distribution(self):
        """ returns dictionary of grades and their cardinality """       
    
        grades_array = []
        for element in self.grades:
            grades_array.append(element['grade'])
        
        seen = {}
        for item in grades_array:
            if not item in seen: 
                seen[item] = 1
                continue
            seen[item] += 1
        
        grades_array = [{'A+': 0}, {'A':0}, {'A-': 0}, {'B+': 0}, {'B': 0}, {'B-': 0}, {'C+': 0}, {'C': 0}, {'C-': 0}, {'F': 0}, {'D N': 0}, {'W': 0}]
        for grade in grades_array:
            for letter in grade:
                try:
                    grade[letter] = seen[letter]
                except:
                    grade[letter] = 0
        return grades_array

    #David and Kevin sort - amazing
    def sort_by_term(self):
        self.grades = sorted(self.grades, cmp=self.compare)

    def compare(self, grade1, grade2):
        terms = {'Fall':0, 'Winter':1, 'Spring':2, 'Summer':3}
        values1 = grade1['term'].split(' ')
        values2 = grade2['term'].split(' ')
        if terms[values1[0]] > terms[values2[0]] or values1[1] > values2[1]: 
            return 1
        else:
            return -1
