import lxml

def advice(html):
    advice = {}
    html = lxml.html.fromstring(html)
    categories = html.xpath('//dd/table/tr/td/a')

    for category in categories:
        classes = []
        code = category.items()[0][1]
        try:
            title = category.getparent().xpath('dl/dt/h4')[0].text_content()
        except:
            title = 'Difference, Power, and Discrimination Courses (3)'
        items = category.getparent().xpath('dl/dd/div/table/tr/td/a')
        for item in items:
            class_items = item.text_content().split(' ')
            classes.append({'discipline':class_items[0], 'number':class_items[1]})

        advice[code] = {'title':title, 'classes':classes}
    return advice
