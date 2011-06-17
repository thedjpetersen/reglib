import lxml.html

def add_class(original_html, crn1, crn2=''):
    html = lxml.html.fromstring(original_html)
    html.get_element_by_id("crn_id1").value = crn1
    html.get_element_by_id("crn_id2").value = crn2
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
