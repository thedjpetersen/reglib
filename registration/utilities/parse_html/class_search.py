import lxml.html

def class_search(original_html, dep, num):
    html = lxml.html.fromstring(original_html)
    try:
        table_element  = html.get_element_by_id('ctl00_ContentPlaceHolder1_SOCListUC1_gvOfferings')
    except:
        return [] 
    table_elements = table_element.getchildren()[1:]
    elements_to_int = ['WL Cap', 'Weeks', 'CRN', 'WL Curr', 'WL Avail', 'Cr']

    classes = []
    
    row_headers = []

    for header in table_element.getchildren()[0].getchildren():
        row_headers.append(header.text_content())

    for row in table_elements:
        one_class = {}
        cells = row.getchildren()
        for index, cell in enumerate(cells):
            content = cell.text_content().strip()

            if row_headers[index] == 'Restrictions' and content != '':
                content = content.split(':')[1]
                content = (' ').join(content.rsplit()).replace(u' College\xc2 Limitations', '').replace('(', '').replace(')','').split(' and ')
                for inner_index, block in enumerate(content):
                    content[inner_index] = block.split(' or ')
                for outer_index, outer_element in enumerate(content):
                    for inner_index, inner_element in enumerate(outer_element):
                        fields = inner_element.split(' ')
                        content[outer_index][inner_index] = {'Department':str(fields[0]), 'Course Number':fields[1]}
            #if row_headers[index] in elements_to_int:
                #content = int(content)

            if row_headers[index] == 'Day/Time/Date' and content != 'TBA':
                fields = content.split(' ')
                days = list(fields[0])
                try:
                    times = fields[1][:9].split('-')
                    for inner_index, time in enumerate(times):
                        times[inner_index] = time[:2] + ':' + time[2:]
                except:
                    times = ''
                try:
                    dates = fields[1][8:]
                except:
                    dates = ''
                content = {"Days":days, "Time":times, "Dates":dates}

            one_class[row_headers[index]] = content
        one_class['Dep'] = dep
        one_class['Num'] = num
        classes.append(one_class)

    return classes