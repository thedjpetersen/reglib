import lxml.html

def get_page_title(original_html):
    html = lxml.html.fromstring(original_html)
    return html.xpath("//title")[0].text_content()
