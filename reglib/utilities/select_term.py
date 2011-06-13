import fetch_html

# CURRENTLY DOESN'T WORK
def select_term(term):
    """ change focus of infosu to different term"""

    html = fetch_html.setup_term_page()
    html = fetch_html.select_term(term)    

