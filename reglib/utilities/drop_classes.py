import fetch_html
import parse_html
from login import login

def drop_classes(sid, pin, crn_list, schedule):
    """ drops a class, takes a crn or two for lec/lab """

    login_number = 2
    for i in range(login_number):
        html = fetch_html.setup_add_drop_page()
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
        values = parse_html.drop_classes(html, crn_list)
        return values
        
