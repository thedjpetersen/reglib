from time_conflict import time_conflict

def class_search_conflict(class1, class2):
    if (set(class1['Times']['Days']).intersection(class2['Times']['Days']) and time_conflict(class1['Times']['Time'], class2['Times']['Time'])):
        return True
    return False
