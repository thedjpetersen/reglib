from re import match, findall, compile

# puts course in ABC 123 format
def format_course(course):
    course_regex = compile('(\w+?)(\d+)')
    if course_regex.match(course):
        match = course_regex.findall(course)
        return match[0][0] + " " + match[0][1]
    return course

def course_to_dep_and_num(course):
    course_regex = compile('(\w+) (\d+)')
    if course_regex.match(course):
        match = course_regex.findall(course)
        return {'department': match[0][0], 'number': match[0][1]}
    return course
