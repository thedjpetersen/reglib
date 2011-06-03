import lxml.html
import re

def class_search(original_html, dep, num):
    html = lxml.html.fromstring(original_html)

    # Get course desc / title via regex
    title_regex = re.compile('\n\s+([\w\s/,]+)\r\s+\(\d\)\.')
    #description_regex = re.compile('\(\d\)\.\s*?<.*?>\s+([\w\s/,\.]+)')
    #description_regex_bacc = re.compile('\(\d\)\.\s*?<img .*?>\s*?</h3>\s+([\w\s/,\.]+)')
    description_regex = re.compile('\(\d\)\.\s*?(<img .*?>)?\s*?</h3>\s+([\w\s/,\.-]+)') # handles bacc core classes
    title = title_regex.findall(original_html)[0]


    description = description_regex.findall(original_html)
    if description:
        description = description[0]
    if description:
        description = description[1]

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
                content = content.split(':')[1].strip().replace('\n', '').replace('\r', '').replace('  ', '')
                '''
                content = (' ').join(content.rsplit()).replace(u' College\xc2 Limitations', '').replace('(', '').replace(')','').split(' and ')
                for inner_index, block in enumerate(content):
                    content[inner_index] = block.split(' or ')
                for outer_index, outer_element in enumerate(content):
                    for inner_index, inner_element in enumerate(outer_element):
                        fields = inner_element.split(' ')
                        content[outer_index][inner_index] = {'Department':str(fields[0]), 'Course Number':fields[1]}
                '''
            #if row_headers[index] in elements_to_int:
                #content = int(content)

            if content != 'TBA':
                if row_headers[index] == 'Day/Time/Date': 
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
                    content = {"days":days, "time":times, "dates":dates}
    
                if row_headers[index] == 'Day/Time/Date':
                    one_class['days'] = content['days']
                    one_class['times'] = content['time']
                    one_class['duration'] = content['dates']
                else:
                    one_class[str.lower(row_headers[index])] = content

        # Change dict keys to standardize and remove spaces for django to access
        keys_to_change = ('cr', 'wl avail', 'avail', 'wl cap', 'wl curr')
        keys_to_use = ('credits', 'wl_available', 'available', 'wl_cap', 'wl_curr')
        for key_orig, key_replace in zip(keys_to_change, keys_to_use): 
            if key_orig in one_class:
                one_class[key_replace] = one_class[key_orig]
                
        one_class['department'] = dep
        one_class['number'] = num

        if description:
            one_class['description'] = description
        if title:
            one_class['title'] = title
        classes.append(one_class)

    return classes
