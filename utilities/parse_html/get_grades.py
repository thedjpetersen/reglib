import lxml.html

def get_grades(original_html):
    html = lxml.html.fromstring(original_html)
    table_elements = html.find_class("datadisplaytable")[0].getchildren()
    
    classes_elements = []
    classes_term = []
    classes = []
    
    for element in table_elements:
        try:
            term = element.find_class("fieldOrangetextbold")[0].text_content()
        except:
            pass

        if len(element.getchildren()) in [6,9]:
            classes_elements.append(element)
            classes_term.append(term)

    for index, element in enumerate(classes_elements):
        text = []
        
        for subelement in element.getchildren():
            text.append(subelement.text_content())
        
        classes.append({'Name' : text[2], 'Department' : text[0], 'Course Number' : text[1], 'Credits' : float(text[3]), 'Grade' : text[4], 'Term' : classes_term[index]})

    return classes
