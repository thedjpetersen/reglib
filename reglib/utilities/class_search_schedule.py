from class_search import class_search
from utilities import time_conflict

def class_search_schedule(dep, num, schedule):
    """ given a course, this goes over the given schedule and 
    see which ones fit """

    terms = {'01':'F', '02':'W', '03':'Sp', '04':'Su'}
    term = terms[schedule.current_term[-2:]] + schedule.current_term[2:4]

    # get list of courses that is the specified course...i hope that makes sense
    search_results = class_search(dep, num, term)
    if not search_results:
        return None 
    
    available_classes = []
    
    # go over every course in the search list and check if it fits in schedule
    for result in search_results:
        flag = False

        if result['available'] <= '0':
            #print "full class"
            continue

        result_days = result['days']
        result_times = result['times']

        # check for conflict against current schedule
        for current_class in schedule.current_classes:
            curr_days = current_class['days']
            curr_time = current_class['time']

            # first check conflict in the day
            if(set(result_days).intersection(curr_days)):
                # then check the specific time
                if time_conflict(result_times, curr_time): 
                    #print ('-').join(result_times) + " conflicts with " + ('-').join(curr_time)
                    flag = True
                #else:
                    #print ('-').join(result_times) + " does not conflict with " + ('-').join(curr_time)
        if not flag:
            available_classes.append(result)

    return available_classes
