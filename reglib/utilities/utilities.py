from re import compile
from typing import Dict, List, Union

# helper functions


def format_course(course: str) -> str:
    """ puts course in [department] [number] format with space """
    course_regex = compile(r'(\w+?)(\d+\w?)')
    if course_regex.match(course):
        match = course_regex.findall(course)
        return f"{match[0][0]} {match[0][1]}"
    return course

def course_to_dep_and_num(course: str) -> Union[Dict[str, str], str]:
    """ separates course into a dictionary with department and number """
    course_regex = compile(r'(\w+) (\d+\w?)')
    if course_regex.match(course):
        match = course_regex.findall(course)
        return {'department': match[0][0], 'number': match[0][1]}
    return course

def time_conflict(time: List[str], time1: List[str]) -> bool:
    """ determine whether two times conflict with format hh:mm """
    if (time[0] >= time1[0] and time[0] <= time1[1]) or (time[1] >= time1[0] and time[1] <= time1[1]):
        return True
    return False

def adjust_schedule_term(infosu_term: str) -> str:
    """ infosu's term years rollover at fall as opposed to winter, need to adjust to match rest of library """
    year = infosu_term[:4]
    term = infosu_term[-2:]

    if term == '00' or term == '01':
        year = str(int(year) - 1)

    return f"{year}{term}"

def format_term(term: str, formal: bool = False) -> str:
    """ format yyyyxx term to Fxx, Wxx, Spxx, Suxx
    or to Fall xxxx, Winter xxxx, Spring xxxx, Summer xxxx if formal """
    year = term[:4]
    term_code = term[-2:]

    if formal:
        term_names = {
            '00': "Summer",
            '01': "Fall",
            '02': "Winter",
            '03': "Spring",
            '04': "Summer"
        }
        term_name = term_names.get(term_code, "")
        return f"{term_name} {year}"
    else:
        year_short = year[-2:]
        term_abbrev = {
            '00': "Su",
            '01': "F",
            '02': "W",
            '03': "Sp",
            '04': "Su"
        }
        term_code_abbrev = term_abbrev.get(term_code, "")
        return f"{term_code_abbrev}{year_short}"


def to_next_term(current_term: str) -> str:
    """ get the next term in YYYYXX format with XX being term from 01 to 04 starting from fall and ending in summer (ex: 201103 is Spring 2011). new school year starts in the fall"""
    year = int(current_term[:4])
    term = int(current_term[-2:])
    # add to term or rollover if summer
    if term != 4:
        term += 1
    else:
        term = 1
    # rollover if current term is summer and next term is fall
    if term == 4:
        year += 1
    next_term = f"{year}0{term}"
    return next_term

def to_prev_term(current_term: str) -> str:
    """ get previous term. used to fetch previous schedules to display in case users want to look back """

    year = int(current_term[:4])
    term = int(current_term[-2:])
    # add to term or rollover if summer
    if term != 1:
        term -= 1
    else:
        term = 4
    # rollback year if current term is fall and previous is summer
    if term == 4:
        year -= 1
    prev_term = f"{year}0{term}"
    return prev_term

