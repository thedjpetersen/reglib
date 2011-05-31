import lxml.html

def get_current_term(original_html):
    html = lxml.html.fromstring(original_html)
    current_term = html.forms[1].getchildren()[0].value_options[0]
    return current_term
