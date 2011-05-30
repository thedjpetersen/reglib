import lxml.html

def get_gpa(original_html):
    html = lxml.html.fromstring(original_html)
  
    osu_gpa = 0
    transfer_gpa = 0
    for element in html.find_class("ddlabel"):
        if element.text_content() == 'Total Institution:':
            osu_gpa = element.getnext().getnext().getnext().getnext().getchildren()[0].text_content()
        if element.text_content() == 'Total Transfer:':
            transfer_gpa = element.getnext().getnext().getnext().getnext().getchildren()[0].text_content()

    return {'osu_gpa': osu_gpa, 'transfer_gpa': transfer_gpa}
             
     
