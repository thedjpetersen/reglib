from browser_clone import header_values, opener
import urllib
import urllib2

def get_calendar(current_term):
    classes_list_url = 'https://adminfo.ucsadm.oregonstate.edu/prod/BWYKFSIC.ics'
    header_values['Referer'] = 'https://adminfo.ucsadm.oregonstate.edu/prod/BWYKFSIC.ics'
    
    form_data = urllib.urlencode({'term_in' : current_term})
    request = urllib2.Request(classes_list_url, form_data, headers=header_values)
    response = opener.open(request)
    html = response.read()
    
    return html
