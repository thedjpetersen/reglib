from class_search import class_search
from class_search_conflict import class_search_conflict

def make_schedule(list_of_classes, term, schedule):
    class_types = ['Lecture', 'WWW']
    
    if term == '':
        terms = {'01':'F', '02':'W', '03':'Sp', '04':'Su'}
        term = terms[schedule.current_term[-2:]] + schedule.current_term[2:4]
    class_search_results = []
    
    for each_class in list_of_classes:
        class_array = each_class.split(' ')
        result_set = class_search(class_array[0], class_array[1], term)
        if type(result_set) is not str:
            new_set = [] 
            for index, result in enumerate(result_set):
                if result['Type'] not in class_types:
                    continue 
                elif not result['Avail'] > 0: 
                    continue 

                new_set.append(result)
                
            class_search_results.append(new_set)

    class_set = []
    combinations = []
    for result_set in class_search_results:
        for result in result_set:
            combinations.append([result])
            for combination in combinations:
                for member in combination:
                    flag = False
                    if member['Dep'] == result['Dep'] and member['Num'] == result['Num']:
                        flag = True 
                    if class_search_conflict(result, member):
                        flag = True 
                if not flag:
                    combination.append(result)

    return combinations
