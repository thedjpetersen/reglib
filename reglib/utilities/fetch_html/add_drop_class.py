from .browser_clone import header_values, opener
import urllib
import urllib.request

def setup_add_drop_page():
    add_drop_page_url = 'https://adminfo.ucsadm.oregonstate.edu/prod/bwskfreg.P_AltPin'
    header_values['Referer'] = 'https://adminfo.ucsadm.oregonstate.edu/prod/twbkwbis.P_GenMenu?name=bmenu.P_RegMnu'
    request = urllib.request.Request(add_drop_page_url, headers = header_values)
    response = opener.open(request)

    html = response.read()
    return html

def current_term_form(current_term):
    return urllib.parse.urlencode({'term_in' : current_term})

def add_drop_page(form_data):
    add_drop_page_url = 'https://adminfo.ucsadm.oregonstate.edu/prod/bwskfreg.P_AltPin'
    header_values['Referer'] = 'https://adminfo.ucsadm.oregonstate.edu/prod/bwskfreg.P_AltPin'
    request = urllib.request.Request(add_drop_page_url, form_data, headers=header_values)
    response = opener.open(request)
    html = response.read()
    return html

def add_class(values):
    #Set up data to be posted
    form_data = urllib.parse.urlencode(values)
    header_values['Referer'] = 'https://adminfo.ucsadm.oregonstate.edu/prod/bwskfreg.P_AltPin'
    submit_url = 'https://adminfo.ucsadm.oregonstate.edu/prod/bwckcoms.P_Regs'

    request = urllib.request.Request(submit_url, form_data, headers=header_values)
    # Request page with CRNs of classes to add
    response = opener.open(request)

    html = response.read()
    return html

def drop_classes(values):
    # Set up data to be posted

    form_data = urllib.parse.urlencode(values)
    header_values['Referer'] = 'https://adminfo.ucsadm.oregonstate.edu/prod/bwskfreg.P_AltPin'
    submit_url = 'https://adminfo.ucsadm.oregonstate.edu/prod/bwckcoms.P_Regs'

    request = urllib.request.Request(submit_url, form_data, headers=header_values)
    # Request page with CRNs of classes to add
    response = opener.open(request)

    html = response.read()
    return html

