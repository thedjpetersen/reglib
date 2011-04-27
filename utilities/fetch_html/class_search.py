from browser_clone import header_values, opener
import urllib
import urllib2

def class_search(dep, num):
    class_url = "http://catalog.oregonstate.edu/CourseDetail.aspx?Columns=abcdfghijklmnopqrstuvwxyz&SubjectCode=" + dep + "&CourseNumber=" + num + "&Campus=corvallis"
        
    response = urllib2.urlopen(class_url)
    if response.url == 'http://catalog.oregonstate.edu/DOE.aspx?Entity=Course':
        return ''
    html = response.read()
    return html
