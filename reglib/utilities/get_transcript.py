import transcript
import parse_html
import fetch_html
from login import login
 
def get_transcript(sid, pin):
    login_number = 2
    for i in range(login_number):  #If we are not logged in we will loop around again
        #The transcript page url
        html = fetch_html.get_transcript()
        
        if parse_html.get_page_title(html) != 'Login':
            # We set the transcript variable to a instance of the transcript class
            grades = parse_html.get_grades(html)
            credits = parse_html.get_credits(html)
            gpa = parse_html.get_gpa(html)
            return transcript.Transcript(html, grades, credits, gpa)
        else:
            login(sid, pin)
