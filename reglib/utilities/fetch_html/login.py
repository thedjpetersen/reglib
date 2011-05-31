from browser_clone import header_values, opener
import urllib
import urllib2


def login(sid, pin):
    header_values['Referer'] = 'https://adminfo.ucsadm.oregonstate.edu/prod/twbkwbis.P_WWWLogin'
        
    #Data to be posted on form
    form_data = urllib.urlencode({'sid' : sid, 'PIN' : pin})
    #The login url
    login_url = 'https://adminfo.ucsadm.oregonstate.edu/prod/twbkwbis.P_ValLogin'

    #build our request and login to set the SESSID cookie
    request = urllib2.Request(login_url, form_data, headers = header_values)
    response = opener.open(request)
    return response.read()
