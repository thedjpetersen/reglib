class Transcript(object):
    def __init__(self, html, grades, credits):
        self.grades = grades
        self.credits = credits

    def has_class(self, dep, cn):
        cn = cn.upper()
        dep = dep.upper()
        for entry in self.grades:
            if entry['Department'] == dep and entry['Course Number'] == cn:
                return entry
        return False

    def has_passed_class(self, dep, cn):
        cn = cn.upper()
        dep = dep.upper()
        passing_grades = ['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C']
        for entry in self.grades:
            if entry['Department'] == dep and entry['Course Number'] == cn and entry['Grade'] in passing_grades:
                return True
        return False

    def grade_distribution(self):
        grades_array = []
        for element in self.grades:
            grades_array.append(element['Grade'])
            grades_array.sort()
        
        seen = {}
        for item in grades_array:
            if not item in seen: 
                seen[item] = 1
                continue
            seen[item] += 1
        
        return seen

