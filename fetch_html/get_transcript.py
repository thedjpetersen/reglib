from browser_clone import header_values, opener
import urllib
import urllib2


def get_transcript():
    trans_url = 'https://adminfo.ucsadm.oregonstate.edu/prod/bwskotrn.P_ViewTran'

    #set up correct header information
    header_values['Referer'] = 'https://adminfo.ucsadm.oregonstate.edu/prod/bwskotrn.P_ViewTermTran'
    header_values['Origin'] = 'https://adminfo.ucsadm.oregonstate.edu'
    form_data = urllib.urlencode({'levl' : '', 'tprt' : 'WWW'})
    request = urllib2.Request(trans_url, form_data, headers = header_values)
    response = opener.open(request)
    html = response.read()
    return html
