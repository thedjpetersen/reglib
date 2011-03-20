import parse_html

class Transcript:
    def __init__(self, html):
        self.grades = parse_html.get_grades(html)
        self.credits = parse_html.get_total_credits(html)
