import fetch_html
import parse_html
from login import login
import reglib

def add_classes(sid, pin, crns, schedule):
    """ registers for a batch of courses. takes a list as a parameter. lecture/lab-rec pairs will be given as a list within the list """

    success_list = []
    for crn_index in crns:
        crn = ''
        crn2 = ''
    
        if 'list' in str(type(crn_index)):
            crn = crn_index[0]
            crn2 = crn_index[1]
        else:
            crn = crn_index

        success = reglib.utilities.add_class(sid, pin, crn, crn2, schedule)
        success_list.append(success)

    return success_list


