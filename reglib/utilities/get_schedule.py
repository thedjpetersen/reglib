import parse_html
import fetch_html
import schedule
from login import login

# Function to set our schedule variable
def get_schedule(sid, pin):
    login_number = 2
    current_term = ''
    for i in range(login_number):
        
        html = fetch_html.setup_schedule_page()
        title = parse_html.get_page_title(html)
        if title != 'Login':
            if title == 'Select Term ':
                current_term = parse_html.get_current_term(html)
            else:
                current_classes = parse_html.get_current_classes(html) 
                return schedule.Schedule(html, current_classes, current_term)
        else:
            login(sid, pin)
            continue

        html = fetch_html.get_schedule(current_term)
        current_classes = parse_html.get_current_classes(html)
        return schedule.Schedule(html, current_classes, current_term)
