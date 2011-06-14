import re

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

    def sort_by_term(self):
        """ given list of courses, sorts by term by most recent """

        fall = []
        summer = []
        spring = []
        winter = []

        fall_regex = re.compile(r"Fall \d\d\d\d")        
        summer_regex = re.compile(r"Summer \d\d\d\d")        
        spring_regex = re.compile(r"Spring \d\d\d\d")        
        winter_regex = re.compile(r"Winter \d\d\d\d")        

        # Sort the whole course of lists by term
        for course in self.grades:
            if fall_regex.search(course['term']):
                fall.append(course)
            if summer_regex.search(course['term']):
                summer.append(course)
            if spring_regex.search(course['term']):
                spring.append(course)
            if winter_regex.search(course['term']):
                winter.append(course)

        # Sort each course by year in each term list
        years = []
        terms = [fall, summer, spring, winter]
        for term in terms:
            for course in term:
                year = (re.findall("\d\d\d\d", course['term']))[0]
                if year not in years:
                    years.append(year)
        years = sorted(years, reverse=True)

        # Sort by year, then term starting with fall (most recent)
        sorted_transcript = []
        for year in years:
            for term in terms:
                for course in term:
                    course_year = (re.findall("\d\d\d\d", course['term']))[0]
                    if course_year == year:
                        sorted_transcript.append(course)
       
        return sorted_transcript 


            
    

        
