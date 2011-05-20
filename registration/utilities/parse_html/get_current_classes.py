import lxml.html
from datetime import datetime

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
        cl["ClassName"] = string_components[0]
        cl["Section"] = string_components[2]
        string_components = string_components[1].split(' ')
        cl["Department"] = string_components[0]
        cl["ClassNumber"] = string_components[1]
        
        class_elements = []
        for index, element in enumerate(each_class[0].getchildren()[1:9]):
            class_elements.append(element.getchildren()[1].text_content())

        cl["Term"] = class_elements[0]
        cl["CRN"] = class_elements[1]
        cl["Registration"] = class_elements[2]
        cl["Instructor"] = class_elements[3].replace('\n','')
        cl["GradingMode"] = class_elements[4]
        cl["Credits"] = float(class_elements[5])
        cl["Level"] = class_elements[6]
        cl["Campus"] = class_elements[7]
        #cl["E-mail"] = each_class[0].getchildren()[4].getchildren()[1].getchildren()[0].attrib['href'].split(':')[1]
        
        class_elements = []
        for index, element in enumerate(each_class[1].getchildren()[2].getchildren()):
            class_elements.append(element.text_content())
        
        cl['Type'] = class_elements[0]
        cl['Time'] = class_elements[1].split(' - ')
        for index, time in enumerate(cl['Time']):
            cl['Time'][index] = datetime.strptime(time, '%I:%M %p').strftime('%H:%M')
        cl['Days'] = list(class_elements[2])
        cl['Location'] = {'Building' : (' ').join(class_elements[3].split(' ')[:-1]), 'Room': class_elements[3].split(' ')[-1]}
        cl['Duration'] = class_elements[4]
        cl['ClassType'] = class_elements[5]
        
        total_classes.append(cl)

    return total_classes
