import fetch_html

def login(sid, pin):
    """ logins, DUH...given sid/pin """

    if len(fetch_html.login(sid, pin))<1000:
        return True
    return False
