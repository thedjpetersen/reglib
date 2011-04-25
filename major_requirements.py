def major_requirements(audit):
    class audit:
        audit_information = dict(audit.xpath('//AuditHeader')[0].items())
        sections = []
        for section in audit.xpath('//Block'):
            items = dict(section.items())
            formatted_items = {'Title':items['Title'], 'Percent Complete':items['Per_complete'], 'Credits Applied':items['Credits_applied'], 'Classes Applied':items['Classes_applied'], 'Requirement ID':items['Req_id'], 'Requirement Value':items['Req_value'], 'Requirement Type':items['Req_type'], 'GPA':items['GPA'], 'GPA Credits':items['Gpa_credits'], 'Cat_yr':items['Cat_yr'],'Cat_yr_start':items['Cat_yr_start'], 'Cat_yrLit':items['Cat_yrLit'], 'GPA points':items['Gpa_grade_pts']}
            rules = []

            for rule in section.xpath('Rule'):
                rules.append(rule_controller(rule))

            formatted_items['Rules'] = rules
            sections.append(formatted_items)

        goals = []
        for item in audit.xpath('Deginfo/Goal'):
            goals.append(dict(item.items()))
        
        temp_dict = dict(audit.xpath('Deginfo/DegreeData')[0].items())
        degree_data = {}
        degree_data['Level'] = temp_dict['Stu_levelLit']
        degree_data['Degree'] = temp_dict['DegreeLit']
        degree_data['Degree Code'] = temp_dict['Degree']
        degree_data['School Code'] = temp_dict['School']
        degree_data['GPA'] = audit_information['DWGPA']
        degree_data['Classes'] = sections[0]['Classes Applied']
        degree_data['Credits'] = sections[0]['Credits Applied']
        degree_data['Email'] = audit_information['Stu_email']

        student_id = audit_information['Stu_id']
        audit_id = audit_information['Audit_id']

    return audit

def rule_controller(rule):
    rule_type = rule.xpath('@RuleType')[0]
    if rule_type == 'Course':
        return course_rule(rule)

def course_rule(rule):
    rule_items = dict(rule.items())
    class rule:
        courses = []
        print rule_items 
        for course in rule.xpath('Advice/Course'):
            courses.append(dict(course.items()))
        name = rule_items['Label']
        percent_complete = rule_items['Per_complete']
        rule_id = rule_items['Rule_id']
        node_type = rule_items['Node_type']
        node_id = rule_items['Node_id']
    
    return rule
