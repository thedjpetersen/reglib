import lxml.html

def get_total_credits(original_html):
    html = lxml.html.fromstring(original_html)
    credits = 0
    for element in html.find_class("ddlabel"):
        if element.text_content() == 'Overall:':
            credits = float(element.getnext().getchildren()[0].text_content())
    return credits
