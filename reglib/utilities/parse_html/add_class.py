import lxml.html

def add_class(original_html, crns=[]):
    html = lxml.html.fromstring(original_html)
    for index, crn in enumerate(crns):
        html.get_element_by_id("crn_id"+str(index+1)).value = crn
    form = html.forms[1]
    #return form.form_values().append(('REG_BTN', 'Submit Changes'))
    values = form.form_values()
    values.append(('REG_BTN', 'Submit Changes'))
    return values 

def add_class_has_errors(original_html):
    html = lxml.html.fromstring(original_html)
    if html.find_class("errortext"):
        return False
    return True
