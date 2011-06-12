import parse_html
import fetch_html
import schedule
from utilities import to_next_term
from login import login

def get_schedule(sid, pin, Next):
    """ Function to set our schedule variable. Get current schedule if next schedule flag not set """
    
    login_number = 2
    term = ''
    for i in range(login_number):
        
        html = fetch_html.setup_schedule_page()
        title = parse_html.get_page_title(html)
        if title != 'Login':
            if title == 'Select Term ':
                term = parse_html.get_current_term(html)
                if Next:
                    term = to_next_term(term)
                    print term
            else:
                courses = parse_html.get_current_classes(html) 
                return schedule.Schedule(html, courses, term)
        else:
            login(sid, pin)
            continue

        html = fetch_html.get_schedule(term)
        courses = parse_html.get_current_classes(html)
        return schedule.Schedule(html, courses, term)
