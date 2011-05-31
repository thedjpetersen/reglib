import lxml.html

def get_credits(original_html):
    # Get dictonary of institution/transfer/total credits


    html = lxml.html.fromstring(original_html)
    institution_credits = 0
    transfer_credits = 0
    total_credits = 0

    for element in html.find_class("ddlabel"):
        if element.text_content() == 'Total Institution:':
            institution_credits = float(element.getnext().getchildren()[0].text_content())
        if element.text_content() == 'Total Transfer:':
            transfer_credits = float(element.getnext().getchildren()[0].text_content())
        if element.text_content() == 'Overall:':
            total_credits = float(element.getnext().getchildren()[0].text_content())
    credits = {'institution_credits': institution_credits, 'transfer_credits': transfer_credits, 'total_credits': total_credits}

    return credits
