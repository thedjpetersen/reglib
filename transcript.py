import parse_html

class Transcript(object):
    def __init__(self, html):
        self.grades = parse_html.get_grades(html)
        self.credits = parse_html.get_total_credits(html)

    def has_class(self, dep, cn):
        cn = cn.capitalize()
        for entry in self.grades:
            if entry['Department'] == dep and entry['Course Number'] == cn:
                return entry
        return False

    def has_passed_class(self, dep, cn):
        cn = cn.capitalize()
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
        result = []
        for item in grades_array:
            if item in seen: continue
            seen[item] = 1
            result.append(item)
        
        return result

