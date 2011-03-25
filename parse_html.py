import lxml.html

def get_grades(original_html):
    html = lxml.html.fromstring(original_html)
    table_elements = html.find_class("datadisplaytable")[0].getchildren()
    
    classes_elements = []
    classes_term = []
    classes = {}
    
    for element in table_elements:
        try:
            term = element.find_class("fieldOrangetextbold")
        except:
            pass

        if len(element.getchildren()) in [6,9]:
            classes_elements.append(element)
            classes_term.append(term)

    for index, element in enumerate(classes_elements):
        text = []
        
        for subelement in element.getchildren():
            text.append(subelement.text_content())
        
        classes[index] = {'Name' : text[2], 'Department' : text[0], 'Course Number' : text[1], 'Credits' : float(text[3]), 'Grade' : text[4], 'Term' : classes_term[index]}

    return classes

def get_total_credits(original_html):
    html = lxml.html.fromstring(original_html)
    credits = 0
    for element in html.find_class("ddlabel"):
        if element.text_content() == 'Overall:':
            credits = float(element.getnext().getchildren()[0].text_content())
    return credits

def get_current_term(original_html):
    html = lxml.html.fromstring(original_html)
    current_term = html.forms[1].getchildren()[0].value_options[0]
    return current_term

def get_page_title(original_html):
    html = lxml.html.fromstring(original_html)
    return html.xpath("//title")[0].text_content()

deg get_current_classes(original_html):
    html = lxml.html.fromstring(original_html)
