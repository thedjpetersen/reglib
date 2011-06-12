import lxml.html
from re import compile, findall

def class_search(original_html, dep, num):
    html = lxml.html.fromstring(original_html)

    ###################################
    # Get course desc / title via regex
    title_regex = compile('\n\s+([\w\s/,-]+)\r\s+\(\d\)\.')
    description_regex = compile('\(\d\)\.\s*?(<img .*?>)?\s*?(<img .*?>)?\s*?</h3>\s+([\w\s/,\.-]+)') # also handles bacc core classes
    try:
        title = title_regex.findall(original_html)[0]
    except:
        title = None
    try:
        description = description_regex.findall(original_html)[0][2]
    except:
        description = None
    ###################################

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
            else:
                one_class['days'] = 'TBA'
                one_class['times'] = 'TBA'
                one_class['duration'] = 'TBA'
                one_class['location'] = 'TBA'

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
