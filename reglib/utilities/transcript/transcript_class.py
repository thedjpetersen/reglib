import re

class Transcript(object):
    def __init__(self, html, grades, credits, gpa):
        self.grades = grades
        self.credits = credits # dictionary (institution, transfer, overall) 
        self.gpa = gpa # dictionary (osu ,transfer)

    def has_class(self, dep, cn):
        cn = cn.upper()
        dep = dep.upper()
        for entry in self.grades:
            if entry['department'] == dep and entry['number'] == cn:
                return entry
        return False

    def has_passed_class(self, dep, cn):
        cn = cn.upper()
        dep = dep.upper()
        passing_grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']
        for entry in self.grades:
            if entry['department'] == dep and entry['number'] == cn and entry['grade'] in passing_grades:
                return True
        return False

    def grade_distribution(self):
        grades_array = []
        for element in self.grades:
            grades_array.append(element['grade'])
            grades_array.sort()
        
        seen = {}
        for item in grades_array:
            if not item in seen: 
                seen[item] = 1
                continue
            seen[item] += 1
        
        return seen

    def sort_by_term(self):

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


            
    

        
