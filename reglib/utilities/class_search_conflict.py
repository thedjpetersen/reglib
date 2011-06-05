from utilities import time_conflict 

def class_search_conflict(class1, class2):
    """ checks if two given classes coincide within the same time, depends on time_conflict """

    # some exception handling
    if 'days' in class1 and 'days' in class2 and 'times' in class1 and 'times' in class2:
        if (set(class1['days']).intersection(class2['days']) and utilities.time_conflict(class1['times'], class2['times'])):
            return True
    return False
