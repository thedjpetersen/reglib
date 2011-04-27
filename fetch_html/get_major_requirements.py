from browser_clone import header_values, opener
import urllib
import urllib2

def infosu_mydegrees_redirect():
    form_page = "https://adminfo.ucsadm.oregonstate.edu/prod/bwykg_dwssbstudent.P_SignOn"
    header_values['Referer'] = "https://adminfo.ucsadm.oregonstate.edu/prod/twbkwbis.P_GenMenu?name=bmenu.P_AdminMnu"

    # Get request page for the form
    request = urllib2.Request(form_page, headers = header_values)
    response = opener.open(request)
    html = response.read()
    return html
    
def first_page_set_cookie(form_list):
    form_data = urllib.urlencode(form_list)
    # Get first page from mydegrees
    mydegrees_url = "https://mydegrees.oregonstate.edu/IRISLink.cgi"
    header_values['Referer'] = "https://adminfo.ucsadm.oregonstate.edu/prod/bwykg_dwssbstudent.P_SignOn"

    request = urllib2.Request(mydegrees_url, form_data, headers= header_values)
    response = opener.open(request)

    header_values['Referer'] = "https://mydegrees.oregonstate.edu/SD_LoadFrameForm.html"

    form_data = urllib.urlencode({'SERVICE':'SCRIPTER','SCRIPT':'SD2STUCON'})
    request = urllib2.Request(mydegrees_url, form_data, headers = header_values)
    response = opener.open(request)
    html = response.read() #final form is in html.forms[7].form_values()
    return html

def form_variables(form_list):
    mydegrees_url = "https://mydegrees.oregonstate.edu/IRISLink.cgi"
    form_data = urllib.urlencode(form_list)
    request = urllib2.Request(mydegrees_url, form_data, headers= header_values)
    response = opener.open(request)
    html = response.read()
    return html
    
def get_xml(form_list):
    mydegrees_url = "https://mydegrees.oregonstate.edu/IRISLink.cgi"
    # Construct variables to post 
    form_data = urllib.urlencode(form_list)
    request = urllib2.Request(mydegrees_url, form_data, headers= header_values) 
    # Make request for degree audit xml from mydegrees
    response = opener.open(request)
    xml = response.read()
    return xml
