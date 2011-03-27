import parse_html

class Schedule(object):
    def __init__(self, html):
       self.current_classes = parse_html.get_current_classes(html) 
