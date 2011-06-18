import lxml.html

def drop_classes(original_html, crn_list):
    html = lxml.html.fromstring(original_html)

    course_table = html.find_class("datadisplaytable")[0]

    # make a list of crns in the order on the website to match them up
    # with the enumerated form values
    infosu_crns = []
    for element in course_table.find_class('dddefault'):
        try:
            crn = element.getchildren()[1]._value__get()
            if crn: 
                infosu_crns.append(crn)
        except:
            pass
 
#    for element in [element.getchildren()[0]._value__get() for element in course_table.find_class('dddefault') if type(element.getchildren()[0]) is lxml.html.InputElement]: 
#        if 'DUMMY' in element and len(temp_list) > 0:
#            course_list.append(temp_list)
#            temp_list = []
#        elif 'DUMMY' not in element:
#            temp_list.append(element)

    # with the list of crns from the website in order, we can make a list
    # of form values to submit and drop
    action_id_list = []
    for crn in crn_list:
        for index, infosu_crn in enumerate(infosu_crns):
            if crn == infosu_crn:
                action_id_list.append("action_id" + str(index+1)) # action_id starts at 1
                break

    
    # set each course to drop in the dropdown boxes (from value '' to 'DX')
    for action_id in action_id_list:
        html.get_element_by_id(action_id)._value__set('DX') # set to drop

    form = html.forms[1]
    values = form.form_values()
    values.append(('REG_BTN', 'Submit Changes'))
                
    return values

