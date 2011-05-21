from class_search import class_search
from time_conflict import time_conflict

def class_search_schedule(dep, num, schedule):
    terms = {'01':'F', '02':'W', '03':'Sp', '04':'Su'}
    term = terms[schedule.current_term[-2:]] + schedule.current_term[2:4]

    search_results = class_search(dep, num, term)
    # If no classes are found, the function will return a string
    if type(search_results) is str:
        return search_results
    
    available_classes = []

    for result in search_results:
        flag = False
        # If the class is full
        if result['Avail'] <= '0':
            print "Full class"
            continue
        result_days = result['Times']['Days']
        result_times = result['Times']['Time']
        for current_class in schedule.current_classes:
            curr_days = current_class['Days']
            curr_time = current_class['Time']
            if(set(result_days).intersection(curr_days)):
                #If we have a conflict set the flag 
                if time_conflict(result_times, curr_time): 
                    print ('-').join(result_times) + " conflicts with " + ('-').join(curr_time)
                    flag = True
                else:
                    print ('-').join(result_times) + " does not conflict with " + ('-').join(curr_time)
        if not flag:
            # If no conflict appned to results(flag unset)
            available_classes.append(result)

    return available_classes
