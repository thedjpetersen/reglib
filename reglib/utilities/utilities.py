from re import match, findall, compile

# helper functions

def format_course(course):
    """ puts course in [department] [number] format with space """
    course_regex = compile('(\w+?)(\d+\w?)')
    if course_regex.match(course):
        match = course_regex.findall(course)
        return match[0][0] + " " + match[0][1]
    return course

def course_to_dep_and_num(course):
    """ separates course into a dictionary with department and number """
    course_regex = compile('(\w+) (\d+\w?)')
    if course_regex.match(course):
        match = course_regex.findall(course)
        return {'department': match[0][0], 'number': match[0][1]}
    return course

def time_conflict(time, time1):
    """ determine whether two times conflict with format hh:mm """
    if (time[0] >= time1[0] and time[0] <= time1[1]) or (time[1] >= time1[0] and time[1] <= time1[1]):
        return True
    return False

def adjust_schedule_term(infosu_term):
    """ infosu's term years rollover at fall as opposed to winter, need to adjust to match rest of library """
    year = infosu_term[:4]
    term = infosu_term[-2:]

    if term == '00' or term == '01':
        year = str(int(year)-1)

    return year + term

def format_term(term):
    """ format yyyyxx term to Fxx, Wxx, Spxx, Suxx """

    year = term[:4][-2:]
    term = term[-2:]
    if term == '00':
        term = "Su"
    elif term == '01':
        term = "F"
    elif term == '02':
        term = "W"
    elif term == '03':
        term = "Sp"
    elif term == '04':
        term = "Su"
      
    return term + year

def to_next_term(current_term):
    """ get the next term in YYYYXX format with XX being term from 01 to 04 starting from fall and ending in summer (ex: 201103 is Spring 2011). new school year starts in the fall"""
    year = int(current_term[:4])
    term = int(current_term[-2:])
    # add to term or rollover if summer
    if term != '04':
        term += 1
    else:
        term = 1
    # rollover if current term is summer and next term is fall
    if term == 4:
        year += 1
    next_term = str(year) + '0' + str(term)
    return next_term

def to_prev_term(current_term):
    """ get previous term. used to fetch previous schedules to display in case users want to look back """

    year = int(current_term[:4])
    term = int(current_term[-2:])
    # add to term or rollover if summer
    if term != '04':
        term -= 1
    else:
        term = 4
    # rollback year if current term is fall and previous is summer
    if term == 1:
        year -= 1
    next_term = str(year) + '0' + str(term)
    return next_term

        
        
    
      
        
        
    
      
