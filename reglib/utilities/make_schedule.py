from class_search import class_search
from class_search_conflict import class_search_conflict

def make_schedule(list_of_classes, term, schedule):
    class_types = ['Lecture', 'WWW']
    lab_types =  ['Recitation', 'Laboratory']
    if term == '':
        terms = {'01':'F', '02':'W', '03':'Sp', '04':'Su'}
        term = terms[schedule.current_term[-2:]] + schedule.current_term[2:4]
    class_search_results = []
    
    for each_class in list_of_classes:
        class_array = each_class.split(' ')
        result_set = class_search(class_array[0], class_array[1], term)
        if type(result_set) is not str:
            new_set = [] 
            rec_lab = []
            for index, result in enumerate(result_set):
                if result['Type'] in lab_types and result['Avail'] > 0:
                    rec_lab.append(result)
                if result['Type'] not in class_types:
                    continue 
                elif not result['Avail'] > '0': 
                    continue 

                new_set.append(result)
            
            if len(rec_lab) > 0:
                class_search_results.append(rec_lab)
            class_search_results.append(new_set)

    class_set = []
    combinations = []
    for result_set in class_search_results:
        for result in result_set:
            combinations.append([result])
            
            is_lab = False
            if result['Type'] in lab_types:
                is_lab = True

            for inner_index, combination in enumerate(combinations):
                for index, member in enumerate(combination):
                    flag = False

                    if member['department'] == result['department'] and member['course_number'] == result['course_number'] and member['Type'] == result['Type']:
                        flag = True 
                    if class_search_conflict(result, member):
                        flag = True 
                        # If the class is the same, but of a different type
                        # Like the difference between a recitation and a lecture
                        # Remove
                        if member['department'] == result['department'] and member['course_number'] == result['course_number'] and member['Type'] != result['Type'] and index == len(combination)-1:
                            combination.remove(member)
                        
                if not flag:
                    combination.append(result)

    return {"combinations" : combinations, "classes_possible" : len(class_search_results)}
