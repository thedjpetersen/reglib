import lxml.html

def drop_classes(original_html, crn_list):
    html = lxml.html.fromstring(original_html)

    course_table = html.find_class("datadisplaytable")[0]

    # make a list of courses (which are lists of input values). use the index
    # drop course since the form value will be action_id[number]
    temp_list = []
    course_list = []
    for element in [element.getchildren()[0]._value__get() for element in course_table.find_class('dddefault') if type(element.getchildren()[0]) is lxml.html.InputElement]: 
        if 'DUMMY' in element and len(temp_list) > 0:
            course_list.append(temp_list)
            temp_list = []
        elif 'DUMMY' not in element:
            temp_list.append(element)


    print course_list
    

