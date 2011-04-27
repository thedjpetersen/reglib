import lxml.html

def mydegrees_redirect_form(original_html):
    html = lxml.html.fromstring(original_html)
    return html.forms[1].form_values()

def mydegrees_form_mangler(original_html):
    html = lxml.html.fromstring(original_html)
    big_form = dict(html.forms[7].form_values())
    big_form['SCRIPT'] = 'SD2AUDCON'
    return big_form 
   
def mydegrees_final_form(original_html):
    html = lxml.html.fromstring(original_html)
    form = dict(html.forms[0].form_values())
    del(form['GETPDF'])
    del(form['PDFContentType'])
    form['REPORT'] = 'WEB31'
    form['SCRIPT'] = 'SD2GETAUD&ContentType=xml'
    form['ContentType'] = 'xml'
    form['BROWSER'] = 'NOT-NAV4'
    form['ACTION'] = 'REVAUDIT'

    return form
