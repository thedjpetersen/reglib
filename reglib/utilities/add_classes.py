import fetch_html
import parse_html
from login import login

def add_classes(sid, pin, crns, schedule):
    """ registers for a batch of courses. takes a list as a parameter. lecture/lab-rec pairs will be given as a list within the list """

    for crn_index in crns:
        crn = ''
        crn2 = ''
    
        if 'list' in str(type(crn_index)):
            crn = crn_index[0]
            crn2 = crn_index[1]
        else:
            crn = crn_index
        
        login_number = 2
        for i in range(login_number):
            html = fetch_html.setup_ad_page()
            title = parse_html.get_page_title(html)
            form_data = ''
            if title != 'Login':
                # a drop down box asks which term to register for. will need to implement for future terms
                if title == 'Select Term ':
                    schedule.current_term = parse_html.get_current_term(html)
                    form_data = fetch_html.current_term_form(schedule.current_term)
            else:
                login(sid, pin)
                continue
            
            html = fetch_html.add_drop_page(form_data)
            # Get a dictionary of values to post as the form
            values = parse_html.add_class(html, crn, crn2)
            html = fetch_html.add_class(values)
            
            # See if there were any errors when posting the form
    
    return parse_html.add_class_has_errors(html) 
