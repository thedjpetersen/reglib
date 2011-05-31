import fetch_html
import parse_html
from login import login

# Function to set our schedule variable
def get_calendar(sid, pin, current_term):
    login_number = 2
    for i in range(login_number):
        
        html = fetch_html.get_calendar(current_term)
        if len(html) <  2000:
            return html
        else:
            login(sid, pin)
            continue

        html = fetch_html.get_calendar(current_term)
        return html
