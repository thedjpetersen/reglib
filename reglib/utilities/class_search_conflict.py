from time_conflict import time_conflict

def class_search_conflict(class1, class2):
    if (set(class1['days']).intersection(class2['days']) and time_conflict(class1['times'], class2['times'])):
        return True
    return False
