from class_search import class_search
from class_search_conflict import class_search_conflict 
from utilities import format_course, adjust_schedule_term

def make_schedule(list_of_classes, term, schedule):
    """ given a list of classes, returns all possible schedule combinations
    such that there are no conflicts. brute force """

    class_types = ['Lecture', 'WWW']
    lab_types =  ['Recitation', 'Laboratory']
    if term == '':
        adjusted_term = adjust_schedule_term(schedule.current_term)
        terms = {'00':'F', '01':'W', '02':'Sp', '03':'Su'}
        term = terms[adjusted_term[-2:]] + adjusted_term[2:4] 
    class_search_results = []

    for each_class in list_of_classes:

        each_class = format_course(each_class)

        # separate courses and get each course's info
        class_array = each_class.split(' ')
        result_set = class_search(class_array[0], class_array[1], term)

        if type(result_set) is not str:
            new_set = [] 
            rec_lab = []
            if result_set is None:
                continue
            for index, result in enumerate(result_set):
                if result['type'] in lab_types and result['available'] > 0:
                    rec_lab.append(result)
                if result['type'] not in class_types:
                    continue 
                elif not result['available'] > '0': 
                    continue 

                new_set.append(result)
            
            if len(rec_lab) > 0:
                class_search_results.append(rec_lab)
            class_search_results.append(new_set)

    class_set = []
    combinations = []

    for res_set in class_search_results:
        for result in res_set:

    for result_set in class_search_results:
        for result in result_set:
            combination = [result]
            
            for class_set in (class_search_results):
                for index, member in enumerate(class_set):
                    flag = False

                    if (member['department'] == result['department'] and member['number'] == result['number']) and ((member['type'] in class_types and result['type'] in class_types) or (member['type'] in lab_types and result['type'] in lab_types)):
                        flag = True 
                    if class_search_conflict(result, member):
                        flag = True 
                        # If the class is the same, but of a different type
                        # Like the difference between a recitation and a lecture
                        # Remove
                        if member['department'] == result['department'] and member['number'] == result['number'] and member['type'] != result['type'] and index == len(combination)-1:
                            combination.remove(member)
                        
                if not flag:
                    combination.append(member)

            combinations.append(combination)

    return {"combinations" : combinations, "classes_possible" : len(class_search_results)}
