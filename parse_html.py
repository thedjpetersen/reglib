import lxml.html

def get_grades(original_html):
    html = lxml.html.fromstring(original_html)
    table_elements = html.find_class("datadisplaytable")[0].getchildren()
    
    classes_elements = []
    classes = {}
    
    for element in table_elements:
        if len(element.getchildren()) in [6,9]:
            classes_elements.append(element)
    
    for index, element in enumerate(classes_elements):
        text = []
        
        for subelement in element.getchildren():
            text.append(subelement.text_content())
        
        classes[index] = {'Name' : text[2], 'Department' : text[0], 'Course Number' : text[1], 'Credits' : float(text[3]), 'Grade' : text[4]}

    return classes

def get_total_credits(original_html):
    html = lxml.html.fromstring(original_html)
    credits = 0
    for element in html.find_class("ddlabel"):
        if element.text_content() == 'Overall:':
            credits = float(element.getnext().getchildren()[0].text_content())
    return credits
