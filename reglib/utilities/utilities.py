from re import match, findall, compile

# helper functions

def format_course(course):
    """ puts course in [department] [number] format with space """
    course_regex = compile('(\w+?)(\d+)')
    if course_regex.match(course):
        match = course_regex.findall(course)
        return match[0][0] + " " + match[0][1]
    return course

def course_to_dep_and_num(course):
    """ separates course into a dictionary with department and number """
    course_regex = compile('(\w+) (\d+)')
    if course_regex.match(course):
        match = course_regex.findall(course)
        return {'department': match[0][0], 'number': match[0][1]}
    return course

def time_conflict(time, time1):
    """ determine whether two times conflict with format hh:mm """
    if (time[0] >= time1[0] and time[0] <= time1[1]) or (time[1] >= time1[0] and time[1] <= time1[1]):
        return True
    return False
