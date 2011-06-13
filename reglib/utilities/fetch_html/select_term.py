from browser_clone import header_values, opener
import urllib
import urllib2

# DOESN'T WORK, perhaps wrong referer
def setup_term_page():

    select_term_url = 'https://adminfo.ucsadm.oregonstate.edu/prod/bwskflib.P_SelDefTerm'
    header_values['Referer'] = 'https://adminfo.ucsadm.oregonstate.edu/prod/twbkwbis.P_GenMenu?name=bmenu.P_RegMnu'

    request = urllib2.Request(select_term_url, headers=header_values)
    response = opener.open(request)
    html = response.read()
    return html

# DOESN'T WORK
def select_term(term):
    """ change the term in the session of which infosu has focus on """

    select_term_url = 'https://adminfo.ucsadm.oregonstate.edu/prod/bwskflib.P_SelDefTerm'
    header_values['Referer'] = 'https://adminfo.ucsadm.oregonstate.edu/prod/twbkwbis.P_GenMenu?name=bmenu.P_RegMnu'

    form_data = urllib.urlencode({'term_in' : term})
    request = urllib2.Request(select_term_url, form_data, headers=header_values)
    response = opener.open(request)
    html = response.read()

    return html
    
