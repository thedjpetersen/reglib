import lxml.html
import re

def get_grades(original_html):
    html = lxml.html.fromstring(original_html)
    table_elements = html.find_class("datadisplaytable")[0].getchildren()
    
    classes_elements = []
    classes_term = []
    classes = []
    
    for element in table_elements:
        try:
            term = element.find_class("fieldOrangetextbold")[0].text_content()
        except:
            pass

        if len(element.getchildren()) in [6,9]:
            classes_elements.append(element)
            classes_term.append(term)

    for index, element in enumerate(classes_elements):
        text = []
        
        for subelement in element.getchildren():
            text.append(subelement.text_content())
        
        classes.append({'Name' : text[2], 'Department' : text[0], 'Course Number' : text[1], 'Credits' : float(text[3]), 'Grade' : text[4], 'Term' : classes_term[index]})

    return classes

def get_total_credits(original_html):
    html = lxml.html.fromstring(original_html)
    credits = 0
    for element in html.find_class("ddlabel"):
        if element.text_content() == 'Overall:':
            credits = float(element.getnext().getchildren()[0].text_content())
    return credits

def get_current_term(original_html):
    html = lxml.html.fromstring(original_html)
    current_term = html.forms[1].getchildren()[0].value_options[0]
    return current_term

def get_page_title(original_html):
    html = lxml.html.fromstring(original_html)
    return html.xpath("//title")[0].text_content()

def get_current_classes(original_html):
    html = lxml.html.fromstring(original_html)
    classes = []
    total_classes = [] 
    elements = html.find_class("datadisplaytable")
    for index in range(0, len(elements), 2):
        classes.append([elements[index], elements[index+1]])
    for loop_index, each_class in enumerate(classes):
        cl = {}
        title_string = each_class[0].find_class("captiontext")[0].text_content()
        string_components = title_string.split(' - ')
        cl["Class Name"] = string_components[0]
        cl["Section"] = string_components[2]
        string_components = string_components[1].split(' ')
        cl["Department"] = string_components[0]
        cl["Class Number"] = string_components[1]
        
        class_elements = []
        for index, element in enumerate(each_class[0].getchildren()[1:9]):
            class_elements.append(element.getchildren()[1].text_content())

        cl["Term"] = class_elements[0]
        cl["CRN"] = class_elements[1]
        cl["Registration"] = class_elements[2]
        cl["Instructor"] = class_elements[3].replace('\n','')
        cl["Grading Mode"] = class_elements[4]
        cl["Credits"] = float(class_elements[5])
        cl["Level"] = class_elements[6]
        cl["Campus"] = class_elements[7]
        #cl["E-mail"] = each_class[0].getchildren()[4].getchildren()[1].getchildren()[0].attrib['href'].split(':')[1]
        
        class_elements = []
        for index, element in enumerate(each_class[1].getchildren()[2].getchildren()):
            class_elements.append(element.text_content())
        
        cl['Type'] = class_elements[0]
        cl['Time'] = class_elements[1]
        cl['Days'] = list(class_elements[2])
        cl['Location'] = {'Building' : (' ').join(class_elements[3].split(' ')[:-1]), 'Room': class_elements[3].split(' ')[-1]}
        cl['Duration'] = class_elements[4]
        cl['Class Type'] = class_elements[5]
        
        total_classes.append(cl)

    return total_classes

def class_search(original_html):
    html = lxml.html.fromstring(original_html)
    table_element  = html.get_element_by_id('ctl00_ContentPlaceHolder1_SOCListUC1_gvOfferings')
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

            if row_headers[index]=='Day/Time/Date':
                fields = content.split(' ')
                days = fields[0]
                time = fields[1][:9]
                dates = fields[1][8:]
                content = {"Days":days, "Time":time, "Dates":dates}
            one_class[row_headers[index]] = content
        classes.append(one_class)

    return classes

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

def get_major_requirements(original_html):
    html = lxml.html.fromstring(original_html)
    html = html.get_element_by_id('ctl00_ContentPlaceHolder1_lblRequirementHTML')
    elements = []
    for element in html.getchildren():
        if element.tag == 'br' and element.tail is not None:
            elements.append(element.tail)
        if element.tag == 'sup' and element.tail is not None:
            elements.append(element.tail)
    return elements

def add_class(original_html, crn, crn2=''):
    html = lxml.html.fromstring(original_html)
    html.get_element_by_id("crn_id1").value = crn
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

