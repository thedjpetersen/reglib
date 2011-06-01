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
        cl["title"] = string_components[0]
        cl["section"] = string_components[2]
        string_components = string_components[1].split(' ')
        cl["department"] = string_components[0]
        cl["number"] = string_components[1]
        
        class_elements = []
        for index, element in enumerate(each_class[0].getchildren()[1:9]):
            class_elements.append(element.getchildren()[1].text_content())

        cl["term"] = class_elements[0]
        cl["crn"] = class_elements[1]
        cl["registration"] = class_elements[2]
        cl["instructor"] = class_elements[3].replace('\n','')
        cl["grading_mode"] = class_elements[4]
        cl["credits"] = float(class_elements[5])
        cl["level"] = class_elements[6]
        cl["campus"] = class_elements[7]
        #cl["E-mail"] = each_class[0].getchildren()[4].getchildren()[1].getchildren()[0].attrib['href'].split(':')[1]
        
        class_elements = []
        for index, element in enumerate(each_class[1].getchildren()[2].getchildren()):
            class_elements.append(element.text_content())
        
        cl['class_type'] = class_elements[0]
        cl['times'] = class_elements[1].split(' - ')
        for index, time in enumerate(cl['times']):
            cl['times'][index] = datetime.strptime(time, '%I:%M %p').strftime('%H:%M')
        cl['days'] = list(class_elements[2])
        cl['location'] = {'building' : (' ').join(class_elements[3].split(' ')[:-1]), 'room': class_elements[3].split(' ')[-1]}
        cl['duration'] = class_elements[4]
        cl['type'] = class_elements[5]
        
        total_classes.append(cl)

    return total_classes
