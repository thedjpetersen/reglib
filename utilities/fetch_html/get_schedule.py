from browser_clone import header_values, opener
import urllib
import urllib2

def setup_schedule_page():
    classes_list_url = 'https://adminfo.ucsadm.oregonstate.edu/prod/bwskfshd.P_CrseSchdDetl'
    header_values['Referer'] = 'https://adminfo.ucsadm.oregonstate.edu/prod/twbkwbis.P_GenMenu?name=bmenu.P_RegMnu'

    request = urllib2.Request(classes_list_url, headers = header_values)
    response = opener.open(request)
    html = response.read()
    return html

def get_schedule(current_term):
    classes_list_url = 'https://adminfo.ucsadm.oregonstate.edu/prod/bwskfshd.P_CrseSchdDetl'
    header_values['Referer'] = 'https://adminfo.ucsadm.oregonstate.edu/prod/twbkwbis.P_GenMenu?name=bmenu.P_RegMnu'
    
    form_data = urllib.urlencode({'term_in' : current_term})
    request = urllib2.Request(classes_list_url, form_data, headers=header_values)
    response = opener.open(request)
    html = response.read()
    
    return html
