from time_conflict import time_conflict

def class_search_conflict(class1, class2):
    if (set(class1['Day/Time/Date']['Days']).intersection(class2['Day/Time/Date']['Days']) and time_conflict(class1['Day/Time/Date']['Time'], class2['Day/Time/Date']['Time'])):
        return True
    return False
